from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('components/pagination.html')
def pagination(page_obj, item_name):
    return {
        'page_obj': page_obj,
        'item_name': item_name
    }

@register.simple_tag
def star_svg():
    return mark_safe(
        '''
<svg style="display:none;">
  <symbol id="star-full" viewBox="0 0 24 24">
    <polygon fill="#FFC107" points="12 2 15.09 8.26 22 9.27
      17 14.14 18.18 21.02 12 17.77 5.82 21.02
      7 14.14 2 9.27 8.91 8.26"/>
  </symbol>

  <symbol id="star-empty" viewBox="0 0 24 24">
    <polygon fill="none" stroke="#FFC107" stroke-width="2" points="12 2 15.09 8.26 22 9.27
      17 14.14 18.18 21.02 12 17.77 5.82 21.02
      7 14.14 2 9.27 8.91 8.26"/>
  </symbol>
</svg>''')