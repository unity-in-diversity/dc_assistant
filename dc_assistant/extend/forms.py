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


# def add_blank_choice(choices):
#     """
#     Добавляет пустое поле в начало выбора
#     """
#     return ((None, '---------'),) + tuple(choices)

# class ColorSelect(forms.Select):
#     """
#     Расширение для встроенного виджета Select чтобы раскрашивать каждую <опцию>.
#     """
#     option_template_name = 'widgets/colorselect_option.html'
#     def __init__(self, *args, **kwargs):
#         kwargs['choices'] = add_blank_choice(COLOR_CHOICES)
#         super().__init__(*args, **kwargs)
#         self.attrs['class'] = 'netbox-select2-color-picker'

#сlass RackAddForm(forms.Form):
#    racktype = forms.MultipleChoiceField(choices=RACK_TYPE_CHOICES, required=True)


# class SlugWidget(forms.TextInput):
#     """
#     Subclass TextInput and add a slug regeneration button next to the form field.
#     """
#     template_name = 'organisation/sluginput.html'
#
# class SlugField(forms.SlugField):
#     """
#     Extend the built-in SlugField to automatically populate from a field called `name` unless otherwise specified.
#     """
#     def __init__(self, slug_source='name', *args, **kwargs):
#         label = kwargs.pop('label', "Slug")
#         help_text = kwargs.pop('help_text', "URL-friendly unique shorthand")
#         widget = kwargs.pop('widget', SlugWidget)
#         super().__init__(label=label, help_text=help_text, widget=widget, *args, **kwargs)
#         self.widget.attrs['slug-source'] = slug_source
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
    Extends the built-in Select widget to colorize each <option>.
    """
    option_template_name = 'colorselect.html'

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = add_blank_choice(COLOR_CHOICES)
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'dc-select2-color-picker'

class ColorField(models.CharField):
    default_validators = [ColorValidator]
    description = "A hexadecimal RGB color code"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorSelect
        return super().formfield(**kwargs)