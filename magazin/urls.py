from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('log/', views.log, name='log'),
    path('despre/', views.despre, name='despre'),
    path('produse/', views.produse, name='produse'),
    path('contact/', views.contact, name='contact'),
    path('cos/', views.cos_virtual, name='cos_virtual'),
    path('in-lucru/', views.in_lucru, name='in_lucru'),
    path("produse/<int:id>/", views.detaliu_produs, name="detaliu_produs"),
    path("categorii/<str:nume_categorie>/",views.produse_dupa_categorie,name="categorie"),
    path("produse/adauga/", views.adauga_produs, name="adauga_produs"),
    path("inregistrare/", views.inregistrare, name="inregistrare"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profil/", views.profil, name="profil"),


]
