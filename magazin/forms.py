from django import forms
from .models import Categorie
from datetime import date
from django.core.exceptions import ValidationError
import re
from .models import Produs
from django.contrib.auth.models import User
from .models import ProfilUtilizator





def validator_nume_produs(value):
    if not value[0].isupper():
        raise ValidationError("Numele produsului trebuie să înceapă cu literă mare.")

def validator_fara_cifre(value):
    if re.search(r"\d", value):
        raise ValidationError("Descrierea nu trebuie să conțină cifre.")
    
class FiltruProduseForm(forms.Form):
    nume = forms.CharField(required=False, label="Nume produs")

    pret_min = forms.FloatField(
        required=False,
        label="Preț minim",
        min_value=0,
        error_messages={"min_value": "Prețul minim nu poate fi negativ."}
    )

    pret_max = forms.FloatField(required=False, label="Preț maxim")

    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        empty_label="Toate categoriile"
    )

    activ = forms.BooleanField(required=False, label="Doar produse active")

    per_page = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=20,
        initial=10,
        label="Produse pe pagină",
        error_messages={
            "min_value": "Trebuie să afișați cel puțin 1 produs pe pagină.",
            "max_value": "Nu puteți afișa mai mult de 20 produse pe pagină."
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        if (
            cleaned_data.get("pret_min") is not None
            and cleaned_data.get("pret_max") is not None
            and cleaned_data["pret_min"] > cleaned_data["pret_max"]
        ):
            raise forms.ValidationError(
                "Prețul minim nu poate fi mai mare decât prețul maxim."
            )
        return cleaned_data




def validare_varsta(value):
    azi = date.today()
    varsta = azi.year - value.year - (
        (azi.month, azi.day) < (value.month, value.day)
    )
    if varsta < 18:
        raise ValidationError("Trebuie să aveți minim 18 ani.")


def validare_numar_cuvinte(value):
    cuvinte = re.findall(r"\b\w+\b", value)
    if len(cuvinte) < 5 or len(cuvinte) > 100:
        raise ValidationError(
            "Mesajul trebuie să conțină între 5 și 100 de cuvinte."
        )


def validare_lungime_cuvant(value):
    for cuvant in value.split():
        if len(cuvant) > 15:
            raise ValidationError(
                f"Cuvântul '{cuvant}' este prea lung (maxim 15 caractere)."
            )


def validare_fara_linkuri(value):
    if "http://" in value or "https://" in value:
        raise ValidationError("Textul nu poate conține linkuri.")


def validare_tip_mesaj(value):
    if value == "":
        raise ValidationError("Selectați un tip de mesaj valid.")


def validare_cnp(value):
    if not value.isdigit():
        raise ValidationError("CNP-ul trebuie să conțină doar cifre.")
    if len(value) != 13:
        raise ValidationError("CNP-ul trebuie să aibă exact 13 cifre.")
    if value[0] not in ["1", "2", "5", "6"]:
        raise ValidationError("CNP invalid.")

def validare_email_temporar(value):
    domenii_interzise = [
        "guerrilla",
        "guerrillamail",
        "tempmail",
        "mailinator",
        "10minute",
        "yopmail",
        "disposable",
    ]

    email_lower = value.lower()

    for domeniu in domenii_interzise:
        if domeniu in email_lower:
            raise ValidationError(
                "Adresele de email temporare nu sunt acceptate."
            )

def validare_text_general(value):
    if not value:
        return  

    if not value[0].isupper():
        raise ValidationError("Textul trebuie să înceapă cu literă mare.")

    if not re.fullmatch(r"[A-Za-zĂÂÎȘȚăâîșț\- ]+", value):
        raise ValidationError(
            "Textul poate conține doar litere, spații și cratimă."
        )

def validare_majuscule_dupa_separator(value):
    if not value:
        return

    for i in range(len(value) - 1):
        if value[i] in [" ", "-"] and value[i + 1].islower():
            raise ValidationError(
                "După spațiu sau cratimă trebuie să urmeze literă mare."
            )




class ContactForm(forms.Form):

    TIPURI = [
        ("", "Neselectat"),
        ("reclamatie", "Reclamație"),
        ("intrebare", "Întrebare"),
        ("review", "Review"),
        ("cerere", "Cerere"),
        ("programare", "Programare"),
    ]

    nume = forms.CharField(
    max_length=10,
    label="Nume",
    validators=[
        validare_text_general,
        validare_majuscule_dupa_separator
        ]
    )
    prenume = forms.CharField(
    max_length=10,
    required=False,
    label="Prenume",
    validators=[
        validare_text_general,
        validare_majuscule_dupa_separator
        ]
    )

    cnp = forms.CharField(
        required=False,
        label="CNP",
        validators=[validare_cnp]
    )

    data_nasterii = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Data nașterii",
        validators=[validare_varsta]
    )

    email = forms.EmailField(label="Email", validators=[validare_email_temporar])
    email_confirmare = forms.EmailField(label="Confirmare email")

    tip_mesaj = forms.ChoiceField(
        choices=TIPURI,
        label="Tip mesaj",
        validators=[validare_tip_mesaj]
    )

    subiect = forms.CharField(
    max_length=100,
    label="Subiect",
    validators=[
        validare_text_general,
        validare_fara_linkuri
        ]
    )

    zile_asteptare = forms.IntegerField(
        min_value=1,
        max_value=30,
        label="Zile de așteptare"
    )

    mesaj = forms.CharField(
        widget=forms.Textarea,
        label="Mesaj (semnați la final)",
        validators=[
            validare_numar_cuvinte,
            validare_lungime_cuvant,
            validare_fara_linkuri
        ]
    )

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("email")
            and cleaned_data.get("email_confirmare")
            and cleaned_data["email"] != cleaned_data["email_confirmare"]
        ):
            self.add_error(
                "email_confirmare",
                "Emailurile nu coincid."
            )

        if (
            cleaned_data.get("mesaj")
            and cleaned_data.get("nume")
            and not cleaned_data["mesaj"].strip().endswith(cleaned_data["nume"])
        ):
            self.add_error(
                "mesaj",
                "Mesajul trebuie să se termine cu numele expeditorului."
            )

        tip = cleaned_data.get("tip_mesaj")
        zile = cleaned_data.get("zile_asteptare")

        if tip == "review" and zile < 4:
            self.add_error("zile_asteptare", "Pentru review minim 4 zile.")

        if tip in ["cerere", "intrebare"] and zile < 2:
            self.add_error(
                "zile_asteptare",
                "Pentru cereri/întrebări minim 2 zile."
            )
        
        cnp = cleaned_data.get("cnp")
        data_nasterii = cleaned_data.get("data_nasterii")

        if cnp and data_nasterii:
            an = int(cnp[1:3])
            luna = int(cnp[3:5])
            zi = int(cnp[5:7])

        if cnp[0] in ["1", "2"]:
            an += 1900
        elif cnp[0] in ["5", "6"]:
            an += 2000
            
        try:
            data_cnp = date(an, luna, zi)
            if data_cnp != data_nasterii:
                self.add_error(
                    "cnp",
                    "CNP-ul nu corespunde cu data nașterii."
                )
        except ValueError:
            self.add_error(
                "cnp",
                "CNP-ul conține o dată invalidă."
            )

        return cleaned_data

class ProdusForm(forms.ModelForm):

    pret_cumparare = forms.FloatField(
        label="Preț de cumpărare",
        help_text="Prețul de achiziție de la furnizor",
        min_value=0
    )

    adaos_percent = forms.IntegerField(
        label="Adaos comercial (%)",
        help_text="Procent de adaos aplicat",
        min_value=1,
        max_value=100
    )

    class Meta:
        model = Produs
        fields = ["nume", "stoc", "activ"]
        labels = {
            "nume": "Denumire produs",
            "descriere": "Descriere produs",
        }
        help_texts = {
            "stoc": "Numărul de bucăți disponibile",
            "activ": "Bifați dacă produsul este activ",
        }
        validators = {
            "nume": [validator_nume_produs],
            "descriere": [validator_fara_cifre],
        }
    def clean_stoc(self):
        stoc = self.cleaned_data.get("stoc")
        if stoc < 0:
            raise ValidationError("Stocul nu poate fi negativ.")
        return stoc

    def clean_adaos_percent(self):
        adaos = self.cleaned_data.get("adaos_percent")
        if adaos > 80:
            raise ValidationError("Adaosul nu poate depăși 80%.")
        return adaos
    
    def clean(self):
        cleaned_data = super().clean()
        pret_c = cleaned_data.get("pret_cumparare")
        adaos = cleaned_data.get("adaos_percent")

        if pret_c and adaos:
            pret_final = pret_c + (pret_c * adaos / 100)
            if pret_final > 1000:
                raise ValidationError(
                    "Prețul final nu poate depăși 1000 lei."
                )

        return cleaned_data

class InregistrareForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    parola = forms.CharField(widget=forms.PasswordInput, label="Parolă")
    confirma_parola = forms.CharField(widget=forms.PasswordInput, label="Confirmă parola")

    telefon = forms.CharField(label="Telefon")
    tara = forms.CharField(label="Țară")
    judet = forms.CharField(label="Județ")
    oras = forms.CharField(label="Oraș")
    adresa = forms.CharField(label="Adresă")

    def clean_telefon(self):
        telefon = self.cleaned_data["telefon"]
        if not re.match(r"^07\d{8}$", telefon):
            raise ValidationError("Telefon invalid. Format: 07XXXXXXXX")
        return telefon

    def clean_parola(self):
        parola = self.cleaned_data["parola"]
        if len(parola) < 6:
            raise ValidationError("Parola trebuie să aibă minim 6 caractere.")
        return parola

    def clean(self):
        cleaned_data = super().clean()
        parola = cleaned_data.get("parola")
        confirma = cleaned_data.get("confirma_parola")

        if parola and confirma and parola != confirma:
            raise ValidationError("Parolele nu coincid.")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Parolă"
    )
    remember_me = forms.BooleanField(
        required=False,
        label="Ține-mă logat"
    )