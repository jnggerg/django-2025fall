from django import template
from django.utils.safestring import mark_safe

register = template.Library()

FULL = '<svg width="20" height="20"><use href="#star-full"/></svg>'
EMPTY = '<svg width="20" height="20"><use href="#star-empty"/></svg>'

@register.filter
def stars(rating):
    rating = int(rating)
    full_stars = FULL * rating
    empty_stars = EMPTY * (5 - rating)
    return mark_safe(full_stars + empty_stars)