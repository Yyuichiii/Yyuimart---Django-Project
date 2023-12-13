from django import template
from datetime import datetime,date



register = template.Library()

@register.filter
def num_format(value):
    if value >= 100000:
        v=value/100000
        return str(str(v)+" Lakh")
    else:
        return value
    



