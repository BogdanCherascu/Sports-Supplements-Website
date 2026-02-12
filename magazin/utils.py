import random
from datetime import datetime, timedelta
from django.core.cache import cache
from .models import Produs

def get_produsul_zilei():
    produs = cache.get("produsul_zilei")

    if produs is None:
        produse = Produs.objects.filter(activ=True)

        if not produse.exists():
            return None

        produs = random.choice(list(produse))

        # expiră la finalul zilei
        now = datetime.now()
        end_of_day = datetime.combine(now.date(), datetime.max.time())
        timeout = int((end_of_day - now).total_seconds())

        cache.set("produsul_zilei", produs, timeout)

    return produs
