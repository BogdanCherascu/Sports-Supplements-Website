from django import template

register = template.Library()

@register.simple_tag
def pret_euro(pret_ron):
    curs = 4.95  
    return round(pret_ron / curs, 2)
