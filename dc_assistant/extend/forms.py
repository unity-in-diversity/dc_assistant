from django import forms
from django.db import models
from django.core.validators import RegexValidator

COLOR_CHOICES = (
    ('aa1409', 'Dark red'),
    ('f44336', 'Red'),
    ('e91e63', 'Pink'),
    ('ffe4e1', 'Rose'),
    ('ff66ff', 'Fuschia'),
    ('9c27b0', 'Purple'),
    ('673ab7', 'Dark purple'),
    ('3f51b5', 'Indigo'),
    ('2196f3', 'Blue'),
    ('03a9f4', 'Light blue'),
    ('00bcd4', 'Cyan'),
    ('009688', 'Teal'),
    ('00ffff', 'Aqua'),
    ('2f6a31', 'Dark green'),
    ('4caf50', 'Green'),
    ('8bc34a', 'Light green'),
    ('cddc39', 'Lime'),
    ('ffeb3b', 'Yellow'),
    ('ffc107', 'Amber'),
    ('ff9800', 'Orange'),
    ('ff5722', 'Dark orange'),
    ('795548', 'Brown'),
    ('c0c0c0', 'Light grey'),
    ('9e9e9e', 'Grey'),
    ('607d8b', 'Dark grey'),
    ('111111', 'Black'),
    ('ffffff', 'White'),
)

ColorValidator = RegexValidator(
    regex='^[0-9a-f]{6}$',
    message='Enter a valid hexadecimal RGB color code.',
    code='invalid'
)

def add_blank_choice(choices):
    """
    Add a blank choice to the beginning of a choices list.
    """
    return ((None, '---------'),) + tuple(choices)


class ColorSelect(forms.Select):
    """
    Extend the built-in Select widget to colorize each option.
    """
    option_template_name = 'colorselect.html'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = add_blank_choice(COLOR_CHOICES)
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'dc-select2-color-picker'


class ColorField(models.CharField):
    """
    Extend CharField to colorize each option if need.
    """
    default_validators = [ColorValidator]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorSelect
        return super().formfield(**kwargs)


class StaticSelectWidget(forms.Select):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'select2 form-control custom-select'

class Select2Multiple(forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attrs['class'] = 'select2 form-control'
        self.attrs['multiple'] = 1

class SlugWidget(forms.TextInput):
    """
    Widget for TextInput. It autocreates value of filed slug by JS
    """
    template_name = 'extend/sluginput.html'


class SlugField(forms.SlugField):
    """
    Extend of SlugField. Let to autocreate value using another field value ('name'). Only for ENG.

    """
    def __init__(self, slug_source='name', *args, **kwargs):
        label = kwargs.pop('label', "Slug")
        widget = kwargs.pop('widget', SlugWidget)
        super().__init__(label=label, widget=widget, *args, **kwargs)
        self.widget.attrs['slug-source'] = slug_source
