from .models import Categorie
import json
import os
from datetime import datetime
from django.conf import settings

def categorii_meniu(request):
    return {
        "categorii_meniu": Categorie.objects.all()
    }

def status_relatii_clienti(request):
    cale = os.path.join(settings.BASE_DIR, "magazin", "data", "program_relatii.json")

    with open(cale, "r", encoding="utf-8") as f:
        program = json.load(f)

    zile = [
        "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]

    acum = datetime.now()
    zi_curenta = zile[acum.weekday()]
    ora_curenta = acum.strftime("%H:%M")

    zi = program.get(zi_curenta)

    mesaj = "Serviciul Relații cu clienții este indisponibil la această oră"

    if zi and not zi.get("closed"):
        start = zi["start"]
        end = zi["end"]

        if start <= ora_curenta <= end:
            mesaj = f"Puteți contacta azi departamentul Relații cu clienții până la ora {end}"

    return {
        "status_relatii_clienti": mesaj
    }