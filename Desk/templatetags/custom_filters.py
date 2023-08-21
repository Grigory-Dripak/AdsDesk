from django import template
from Desk.models import STATUS

register = template.Library()


@register.filter()
def statusname(status):
   i = [j[1] for j in STATUS if j[0]==status]
   return f'{i[0]}'
