from django import forms

# COLOR_CHOICES = (
#     ('aa1409', 'Dark red'),
#     ('f44336', 'Red'),
#     ('e91e63', 'Pink'),
#     ('ffe4e1', 'Rose'),
#     ('ff66ff', 'Fuschia'),
#     ('9c27b0', 'Purple'),
#     ('673ab7', 'Dark purple'),
#     ('3f51b5', 'Indigo'),
#     ('2196f3', 'Blue'),
#     ('03a9f4', 'Light blue'),
#     ('00bcd4', 'Cyan'),
#     ('009688', 'Teal'),
#     ('00ffff', 'Aqua'),
#     ('2f6a31', 'Dark green'),
#     ('4caf50', 'Green'),
#     ('8bc34a', 'Light green'),
#     ('cddc39', 'Lime'),
#     ('ffeb3b', 'Yellow'),
#     ('ffc107', 'Amber'),
#     ('ff9800', 'Orange'),
#     ('ff5722', 'Dark orange'),
#     ('795548', 'Brown'),
#     ('c0c0c0', 'Light grey'),
#     ('9e9e9e', 'Grey'),
#     ('607d8b', 'Dark grey'),
#     ('111111', 'Black'),
#     ('ffffff', 'White'),
# )

# RACK_TYPE_CHOICES = (
#     (1, 'Открытая стойка однорамочная'),
#     (2, 'Открытая стойка двухрамочная'),
#     (3, 'Серверный шкаф напольный'),
#     (4, 'Серверный шкаф настенный'),
#      )

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