from django import template
from magazin.utils import get_produsul_zilei

register = template.Library()

@register.inclusion_tag("magazin/partials/produsul_zilei.html")
def produsul_zilei():
    return {
        "produsul_zilei": get_produsul_zilei()
    }
