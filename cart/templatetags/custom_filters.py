from django import template

register = template.Library()


@register.filter
def format_price(value):
    try:
        value = float(value)
        return "{:,.0f}".format(value)
    except:
        return value