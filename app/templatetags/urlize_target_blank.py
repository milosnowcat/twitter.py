from django import template
from django.utils.html import urlize as urlize_impl
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def urlize_target_blank(value):
    return mark_safe(urlize_impl(value).replace('<a ',
        '<a target="_blank" class="button button--flex button--white" '
    ))

register.filter('urlize_target_blank', urlize_target_blank)