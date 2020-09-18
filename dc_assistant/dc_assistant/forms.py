from django import forms

OBJ_TYPE_CHOICES = (
    ('', 'All Objects'),
    ('Organisation', (
        ('location', 'Location'),
        ('rack', 'Racks'),
        ('vendormodel', 'Device models'),
        ('device', 'Devices'),
    )),
    ('Secret', (
        ('secret', 'Secrets'),
    )),
)

class SearchForm(forms.Form):
    q = forms.CharField(
        label='Search'
    )
    obj_type = forms.ChoiceField(
        choices=OBJ_TYPE_CHOICES, required=False, label='Type'
    )