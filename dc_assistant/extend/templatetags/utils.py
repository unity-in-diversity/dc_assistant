from django import template
import re

register = template.Library()

def foreground_color(bg_color):
    """
    Return the ideal foreground color (black or white) for a given background color in hexadecimal RGB format.
    """
    bg_color = bg_color.strip('#')
    r, g, b = [int(bg_color[c:c + 2], 16) for c in (0, 2, 4)]
    if r * 0.299 + g * 0.587 + b * 0.114 > 186:
        return '000000'
    else:
        return 'ffffff'

@register.filter()
def fgcolor(value):
    """
    Return black (#000000) or white (#ffffff) given an arbitrary background color in RRGGBB format.
    """
    value = value.lower().strip('#')
    if not re.match('^[0-9a-f]{6}$', value):
        return ''
    return '#{}'.format(foreground_color(value))

