from django import template

register = template.Library()


@register.simple_tag()
def hrefcreate(href='http://127.0.0.1:8000/ads/', value=''):
   return f'{href}{value}'


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()
