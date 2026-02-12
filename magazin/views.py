import re
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from urllib.parse import urlparse, parse_qs
from datetime import date, datetime
from .models import Produs, Categorie,Producator
from django import forms
from .forms import FiltruProduseForm, ContactForm,ProdusForm
from django.http import HttpResponseBadRequest, HttpResponse
import json
import os
from django.contrib.auth.models import User
from .forms import InregistrareForm,LoginForm
from .models import ProfilUtilizator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




class Accesare:
    _last_id = 0  

    def __init__(self, ip_client, url, data=None):
        Accesare._last_id += 1
        self.id = Accesare._last_id
        self.ip_client = ip_client
        self._url = url
        self._data = data or datetime.now()

    def lista_parametri(self):
        parsed = urlparse(self._url)
        params = parse_qs(parsed.query)

        lista = []
        for nume, valori in params.items():
            if valori:
                lista.append((nume, valori))
            else:
                lista.append((nume, None))
        return lista

    def url(self):
        return self._url

    def data(self, fmt):
        return self._data.strftime(fmt)

    def pagina(self):
        parsed = urlparse(self._url)
        return parsed.path

log_accesari = []

def afis_data(tip):
    zile_sapt = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    luni = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
            "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]

    acum = datetime.now()

    zi_sapt = zile_sapt[acum.weekday()]    
    zi = acum.day
    luna = luni[acum.month - 1]        
    an = acum.year

    data_formata = f"{zi_sapt}, {zi} {luna} {an}"
    ora_formata = acum.strftime("%H:%M:%S")

    if tip == "zi":
        return f"<h2>Data</h2><p>{data_formata}</p>"
    elif tip == "timp":
        return f"<h2>Ora</h2><p>{ora_formata}</p>"
    else:
        return f"<h2>Data și ora</h2><p>{data_formata} — {ora_formata}</p>"

def index(request):
    ip = request.META.get("REMOTE_ADDR")
    return render(request, "magazin/index.html", {"ip": ip})

def info(request):
    ip = request.META.get("REMOTE_ADDR")
    param = request.GET.get("data")
    parametri = list(request.GET.keys())
    nr_parametri = len(parametri)
    mesaj = ""

    now = datetime.now()

    if param == "ora":
        mesaj = f"Ora curentă este: {now.strftime('%H:%M:%S')}"
    elif param == "zi":
        mesaj = f"Data curentă este: {now.strftime('%d.%m.%Y')}"
    elif param == "timp":
        mesaj = f"Data și ora curentă sunt: {now.strftime('%d.%m.%Y %H:%M:%S')}"
    elif param:
        mesaj = "Parametru necunoscut."

    return render(
        request,
        "magazin/info.html",
        {
            "ip": ip,
            "mesaj": mesaj,
            "nr_parametri": nr_parametri,
            "parametri": parametri,
        }
    )

def despre(request):
    ip = request.META.get("REMOTE_ADDR")
    return render(request, "magazin/despre.html", {"ip": ip})


def produse(request):
    qs = Produs.objects.select_related("categorie")

    form = FiltruProduseForm(request.GET or None)

    mesaj_paginare = None

    if form.is_valid():
        if form.cleaned_data.get("nume"):
            qs = qs.filter(nume__icontains=form.cleaned_data["nume"])

        if form.cleaned_data.get("pret_min") is not None:
            qs = qs.filter(pret__gte=form.cleaned_data["pret_min"])

        if form.cleaned_data.get("pret_max") is not None:
            qs = qs.filter(pret__lte=form.cleaned_data["pret_max"])

        if form.cleaned_data.get("categorie"):
            qs = qs.filter(categorie=form.cleaned_data["categorie"])

        if form.cleaned_data.get("activ"):
            qs = qs.filter(activ=True)

        per_page = form.cleaned_data.get("per_page") or 10

        if per_page != 10:
            mesaj_paginare = (
                "Atenție: schimbarea numărului de produse pe pagină "
                "poate duce la sărirea sau repetarea unor produse."
            )
    else:
        qs = Produs.objects.none()
        per_page = 10

    sort = request.GET.get("sort")

    if sort == "a":
        qs = qs.order_by("pret")
    elif sort == "d":
        qs = qs.order_by("-pret")

    
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "form": form,
        "mesaj_paginare": mesaj_paginare,
    }

    return render(request, "magazin/produse.html", context)
    
def detaliu_produs(request, id):
    produs = get_object_or_404(Produs, id=id)
    return render(
        request,
        "magazin/detaliu_produs.html",
        {"produs": produs}
    )
    
def produse_dupa_categorie(request, nume_categorie):
    categorie = get_object_or_404(Categorie, nume=nume_categorie)

    form = FiltruProduseForm(request.GET or None)
    
    form.fields["categorie"].initial = categorie

    produse = Produs.objects.filter(categorie=categorie)

    if form.is_valid():
        categorie_form = form.cleaned_data.get("categorie")
        if categorie_form and categorie_form != categorie:
            return HttpResponseBadRequest(
                "Eroare: categoria a fost modificată ilegal."
            )

        if form.cleaned_data.get("nume"):
            produse = produse.filter(nume__icontains=form.cleaned_data["nume"])

        if form.cleaned_data.get("pret_min") is not None:
            produse = produse.filter(pret__gte=form.cleaned_data["pret_min"])

        if form.cleaned_data.get("pret_max") is not None:
            produse = produse.filter(pret__lte=form.cleaned_data["pret_max"])

        if form.cleaned_data.get("activ"):
            produse = produse.filter(activ=True)

        per_page = form.cleaned_data.get("per_page") or 5
    else:
        per_page = 5

    

    paginator = Paginator(produse, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "magazin/categorie.html", {
        "categorie": categorie,
        "form": form,
        "page_obj": page_obj,
    })

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            azi = date.today()
            ani = azi.year - data["data_nasterii"].year
            luni = azi.month - data["data_nasterii"].month

            if azi.day < data["data_nasterii"].day:
                luni -= 1
            if luni < 0:
                ani -= 1
                luni += 12

            mesaj_curat = re.sub(r"\s+", " ", data["mesaj"]).strip()

            rezultat = ""
            majuscula = True
            for c in mesaj_curat:
                if majuscula and c.isalpha():
                    rezultat += c.upper()
                    majuscula = False
                else:
                    rezultat += c
                if c in ".?!":
                    majuscula = True

            mesaj_final = rezultat

            minime = {
                "review": 4,
                "cerere": 2,
                "intrebare": 2,
                "reclamatie": 2,
                "programare": 2,
            }

            urgent = data["zile_asteptare"] == minime.get(data["tip_mesaj"], 999)

            date_json = {
                "nume": data["nume"],
                "prenume": data["prenume"],
                "email": data["email"],
                "tip_mesaj": data["tip_mesaj"],
                "subiect": data["subiect"],
                "mesaj": mesaj_final,
                "zile_asteptare": data["zile_asteptare"],
                "varsta": f"{ani} ani și {luni} luni",
                "urgent": urgent,
                "timestamp": datetime.now().isoformat()
            }

            os.makedirs("Mesaje", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nume_fisier = timestamp + ("_urgent.json" if urgent else ".json")

            with open(os.path.join("Mesaje", nume_fisier), "w", encoding="utf-8") as f:
                json.dump(date_json, f, ensure_ascii=False, indent=4)

            return render(request, "magazin/contact_succes.html")

    else:
        form = ContactForm()

    return render(request, "magazin/contact.html", {"form": form})

def cos_virtual(request):
    ip = request.META.get("REMOTE_ADDR")
    return render(request, "magazin/in_lucru.html", {"ip": ip})

def in_lucru(request):
    ip = request.META.get("REMOTE_ADDR")
    return render(request, "magazin/in_lucru.html", {"ip": ip})

def calculeaza_varsta(data_nasterii):
    azi = date.today()

    ani = azi.year - data_nasterii.year
    luni = azi.month - data_nasterii.month

    if azi.day < data_nasterii.day:
        luni -= 1

    if luni < 0:
        ani -= 1
        luni += 12

    return ani, luni

def curata_mesaj(text):
    return re.sub(r"\s+", " ", text).strip()

def majuscule_dupa_punctuatie(text):
    rezultat = ""
    majuscula = True

    for c in text:
        if majuscula and c.isalpha():
            rezultat += c.upper()
            majuscula = False
        else:
            rezultat += c

        if c in ".?!":
            majuscula = True

    return rezultat

def este_urgent(tip, zile):
    minime = {
        "review": 4,
        "cerere": 2,
        "intrebare": 2,
        "reclamatie": 2,
        "programare": 2,
    }

    return zile == minime.get(tip, 999)

def adauga_produs(request):
    if request.method == "POST":
        form = ProdusForm(request.POST)
        if form.is_valid():
            produs = form.save(commit=False)

            pret_c = form.cleaned_data["pret_cumparare"]
            adaos = form.cleaned_data["adaos_percent"]

            produs.pret = pret_c + (pret_c * adaos / 100)
            produs.categorie = Categorie.objects.first()
            produs.producator = Producator.objects.first()

            produs.save()

            return redirect("produse")
    else:
        form = ProdusForm()

    return render(request, "magazin/adauga_produs.html", {"form": form})

def log(request):
    log_request(request)
    

    sql_activ = request.GET.get("sql") == "true"

    sql_queries = []
    nr_sql_curent = 0

    if sql_activ:
        list(Produs.objects.all()[:5])

        sql_queries = connection.queries
        nr_sql_curent = len(sql_queries)

        total_sql = request.session.get("total_sql", 0)
        total_sql += nr_sql_curent
        request.session["total_sql"] = total_sql
    else:
        total_sql = request.session.get("total_sql", 0)


    mesaje = []


    accesari_afisate = log_accesari[:]

    param_ultimele = request.GET.get("ultimele")

    if param_ultimele is not None:
        if not param_ultimele.isdigit():
            mesaje.append("Eroare: parametrul 'ultimele' trebuie să fie un număr întreg.")
        else:
            n = int(param_ultimele)
            total = len(log_accesari)

            if n == 0:
                accesari_afisate = []
            elif n > total:
                mesaje.append(f"Atenție: există doar {total} accesări.")
                accesari_afisate = log_accesari
            else:
                accesari_afisate = log_accesari[-n:]

    param_accesari = request.GET.get("accesari")

    if param_accesari == "nr":
        mesaje.append(f"Număr total accesări: {len(log_accesari)}")

    elif param_accesari == "detalii":
        for acc in log_accesari:
            mesaje.append(acc.data("%d/%m/%Y %H:%M:%S"))

    list_iduri = request.GET.getlist("iduri")

    if list_iduri:
        iduri_expandate = []
        for grupa in list_iduri:
            for id_str in grupa.split(","):
                iduri_expandate.append(id_str)

        iduri_num = []
        for elem in iduri_expandate:
            if elem.isdigit():
                iduri_num.append(int(elem))
            else:
                mesaje.append(f"ID invalid: {elem}")

        param_dubluri = request.GET.get("dubluri", "false").lower()

        if param_dubluri != "true":
            iduri_finale = []
            for x in iduri_num:
                if x not in iduri_finale:
                    iduri_finale.append(x)
        else:
            iduri_finale = iduri_num

        accesari_selectate = []
        for id_cautat in iduri_finale:
            gasit = False
            for acc in log_accesari:
                if acc.id == id_cautat:
                    accesari_selectate.append(acc)
                    gasit = True
                    break
            if not gasit:
                mesaje.append(f"Atenție: accesarea cu ID-ul {id_cautat} nu există.")

        accesari_afisate = accesari_selectate

    contor = {}
    for acc in accesari_afisate:
        pag = acc.pagina()
        contor[pag] = contor.get(pag, 0) + 1

    if contor:
        pagina_max = max(contor, key=contor.get)
        pagina_min = min(contor, key=contor.get)
    else:
        pagina_max = pagina_min = None

    accesari_template = []
    for acc in accesari_afisate:
        accesari_template.append({
            "id": acc.id,
            "url": acc.url(),
            "data": acc.data("%d/%m/%Y %H:%M:%S")
        })
        
    param_tabel = request.GET.get("tabel")

    if param_tabel:
        if param_tabel == "tot":
            coloane_tabel = ["id", "url", "data"]
        else:
            coloane_tabel = param_tabel.split(",")

    return render(
        request,
        "magazin/log.html",
        {
            "ip": request.META.get("REMOTE_ADDR"),
            "accesari": accesari_template,
            "mesaje": mesaje,
            "pagina_max": pagina_max,
            "pagina_min": pagina_min,
            "tabel": param_tabel,
            "coloane_tabel": coloane_tabel,
            
            "sql_activ": sql_activ,
            "sql_queries": sql_queries,
            "nr_sql_curent": nr_sql_curent,
            "total_sql": total_sql,
        }
    )





def log_request(request):
    url_complet = request.get_full_path()
    ip = request.META.get("REMOTE_ADDR")
    acces = Accesare(ip, url_complet)

    log_accesari.append(acces)
    return acces





def inregistrare(request):
    if request.method == "POST":
        form = InregistrareForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["parola"]
            )

            ProfilUtilizator.objects.create(
                user=user,
                telefon=form.cleaned_data["telefon"],
                tara=form.cleaned_data["tara"],
                judet=form.cleaned_data["judet"],
                oras=form.cleaned_data["oras"],
                adresa=form.cleaned_data["adresa"]
            )

            return redirect("login")
    else:
        form = InregistrareForm()

    return render(request, "magazin/inregistrare.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user is not None:
                login(request, user)

                # 🔑 REMEMBER ME
                if form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(60 * 60 * 24)  # 1 zi
                else:
                    request.session.set_expiry(0)  # sesiune browser

                return redirect("profil")
            else:
                form.add_error(None, "Username sau parolă incorecte.")
    else:
        form = LoginForm()

    return render(request, "magazin/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profil(request):
    return render(request, "magazin/profil.html")


# def sql_log(request):
#     afiseaza_sql = request.GET.get("sql") == "true"

#     if afiseaza_sql:
#         list(Produs.objects.all()[:5])
#         queries = connection.queries
#     else:
#         queries = []

#     return render(
#         request,
#         "magazin/sql_log.html",
#         {
#             "queries": queries,
#             "afiseaza_sql": afiseaza_sql
#         }
#     )
