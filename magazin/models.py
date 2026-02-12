from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    descriere = models.TextField()

    culoare = models.CharField(
        max_length=20,
        default="#ff7c23",
        help_text="Culoare HEX, ex: #ff7c23"
    )

    icon = models.CharField(
        max_length=50,
        default="fa-tag",
        help_text="Icon FontAwesome, ex: fa-dumbbell"
    )
    
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categorii"

    def __str__(self):
        return self.nume



class Producator(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    tara_origine = models.CharField(max_length=100)
    an_infiintare = models.IntegerField()
    cifra_afaceri = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Producator"
        verbose_name_plural = "Producatori"

    def __str__(self):
        return self.nume


class Ingredient(models.Model):
    TIP_INGREDIENT = [
        ("activ", "Activ"),
        ("aroma", "Aromă"),
        ("vitamina", "Vitamină"),
        ("altul", "Altul"),
    ]

    nume = models.CharField(max_length=100)
    descriere = models.TextField()
    tip = models.CharField(
        max_length=20,
        choices=TIP_INGREDIENT,
        default="altul"
    )
    
    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingrediente"

    def __str__(self):
        return self.nume


class Oferta(models.Model):
    data_incepere = models.DateField()
    data_finalizare = models.DateField()
    procentaj = models.IntegerField()
    
    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Oferte"

    def __str__(self):
        return f"Reducere {self.procentaj}%"


class Produs(models.Model):
    nume = models.CharField(max_length=150)
    pret = models.FloatField()
    stoc = models.IntegerField(default=0)
    activ = models.BooleanField(default=True)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="produse"
    )

    producator = models.ForeignKey(
        Producator,
        on_delete=models.CASCADE,
        related_name="produse"
    )

    ingrediente = models.ManyToManyField(
        Ingredient,
        blank=True
    )

    oferte = models.ManyToManyField(
        Oferta,
        blank=True
    )

    data_adaugare = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Produs"
        verbose_name_plural = "Produse"

    def __str__(self):
        return self.nume
    
    
class ProfilUtilizator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    telefon = models.CharField(max_length=20)
    adresa = models.CharField(max_length=100)
    oras = models.CharField(max_length=50)
    judet = models.CharField(max_length=50)
    tara = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = "Profil Utilizaror"
        verbose_name_plural = "Profil Utilizatori"

    def __str__(self):
        return f"Profil {self.user.username}"
