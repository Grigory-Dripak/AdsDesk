from django import template
from AdsDesk.settings import SITE_URL
register = template.Library()


@register.simple_tag()
def hrefcreate(href={SITE_URL}, upath='/ads/', value=''):
   return f'{href}{upath}{value}'


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
