from django import template
from django.urls import reverse
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

@register.inclusion_tag('extend/tag.html')
def tag(tag, url_name=None):
    """
    Display a tag, optionally linked to a filtered list of objects.
    """
    return {
        'tag': tag,
        'url_name': url_name,
    }

def _get_viewname(instance, action):
    """
    Return the appropriate viewname for adding, editing, or deleting an instance.
    """
    # Validate action
    assert action in ('add', 'edit', 'delete')
    viewname = "{}:{}_{}".format(
        instance._meta.app_label, instance._meta.model_name, action
    )
    return viewname

@register.inclusion_tag('extend/edit.html')
def edit_button(instance, use_pk=False):
    viewname = _get_viewname(instance, 'edit')

    # Assign kwargs
    if hasattr(instance, 'slug') and not use_pk:
        kwargs = {'slug': instance.slug}
    else:
        kwargs = {'pk': instance.pk}

    url = reverse(viewname, kwargs=kwargs)

    return {
        'url': url,
    }

@register.filter()
def decryptable_by(secret, user):
    """
    Determine whether a given User is permitted to decrypt a Secret.
    """
    return secret.decryptable_by(user)
