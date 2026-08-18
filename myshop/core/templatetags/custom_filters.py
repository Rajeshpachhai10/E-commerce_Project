from django import template
from django.utils.html import strip_tags
import html

register = template.Library()

@register.filter
def clean_desc(value, word_limit=15):
    if not value:
        return ""
    unescaped = html.unescape(str(value))   # turns &lt; back into 
    plain = strip_tags(unescaped)            # now real tags can be stripped
    words = plain.split()
    return " ".join(words[:word_limit]) + ("..." if len(words) > word_limit else "")