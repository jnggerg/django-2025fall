import math
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

@register.filter
def avg_rating(reviews):

    # need to call .all since RelatedManager is not iterable directly
    if hasattr(reviews, 'all'):
        reviews = reviews.all()
    
    reviews_list = list(reviews)
    if len(reviews_list) == 0:
        return stars(0)
    
    total = sum(review.rating for review in reviews_list)
    avg = math.floor(total / len(reviews_list))
    return stars(avg)
    

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()