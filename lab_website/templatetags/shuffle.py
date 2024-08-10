
#from  https://stackoverflow.com/questions/28837511/django-template-how-to-randomize-order-when-populating-page-with-objects
import random
from django import template
register = template.Library()

@register.filter
def shuffle(arg):
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux