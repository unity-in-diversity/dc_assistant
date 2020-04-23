from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Region

class RegionAddForm(forms.ModelForm):
    parent = TreeNodeChoiceField(required=False, queryset=Region.objects.all(), level_indicator = u'--',)
    name = forms.CharField(label='Название региона')
    slug = forms.CharField(label='Псевдоним без пробелов')

    class Meta:
        model = Region
        fields = (
            'parent', 'name', 'slug',
        )