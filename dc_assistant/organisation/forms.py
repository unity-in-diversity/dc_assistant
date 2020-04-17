from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Region, Location

class RegionAddForm(forms.ModelForm):
    parent = TreeNodeChoiceField(label='Родитель', required=False, queryset=Region.objects.all(), level_indicator = u'-', widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Название региона')
    slug = forms.CharField(label='Псевдоним')

    class Meta:
        model = Region
        fields = (
            'parent', 'name', 'slug',
        )

class SiteAddForm(forms.ModelForm):
    name = forms.CharField()
    slug = forms.SlugField()
    region = TreeNodeChoiceField(
        label='Регион',
        queryset=Region.objects.all(),
        required=False,
        level_indicator=u'-',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    physical_address = forms.CharField
    description = forms.CharField
    comment = forms.CharField


    class Meta:
        model = Location
        fields = [
            'name', 'slug', 'region', 'physical_address', 'description', 'comment'
        ]
        widgets = {
            'physical_address': forms.Textarea(attrs={'rows': 3,}),
            'description': forms.Textarea(attrs={'rows': 3, }),
            'comment': forms.Textarea(attrs={'rows': 5, })
        }

