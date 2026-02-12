from django.contrib import admin
from .models import Categorie, Producator, Produs, Ingredient, Oferta, ProfilUtilizator

admin.site.register(Categorie)
admin.site.register(Producator)

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ("nume", "pret", "stoc", "activ", "categorie", "producator")
    search_fields = ("nume", "categorie__nume", "producator__nume")
    list_filter = ("activ", "categorie", "producator")
    ordering = ("nume", "pret")
    list_per_page = 5

    readonly_fields = ("data_adaugare",)

    fieldsets = (
        ("Informații principale", {
            "fields": ("nume", "pret", "stoc", "activ")
        }),
        ("Relații", {
            "fields": ("categorie", "producator", "ingrediente", "oferte")
        }),
        ("Altele", {
            "fields": ("data_adaugare",),
            "classes": ("collapse",)
        }),
    )

admin.site.register(Ingredient)
admin.site.register(Oferta)
admin.site.register(ProfilUtilizator)

admin.site.site_header = "Administrare Magazin Suplimente"
admin.site.site_title = "Admin Suplimente"
admin.site.index_title = "Panou de administrare"

