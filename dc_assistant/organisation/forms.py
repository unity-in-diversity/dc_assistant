from django import forms
from mptt.forms import TreeNodeChoiceField
from taggit.forms import TagField
from .models import Region, Location, Rack

class StaticSelectWidget(forms.Select):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'select2 form-control custom-select'

class RegionAddForm(forms.ModelForm):
    parent = TreeNodeChoiceField(label='Родитель', required=False, queryset=Region.objects.all(), level_indicator = u'-', widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Название региона')
    slug = forms.CharField(label='Псевдоним')

    class Meta:
        model = Region
        fields = (
            'parent', 'name', 'slug',
        )

class LocationAddForm(forms.ModelForm):
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
            'physical_address': forms.Textarea(attrs={'rows': 3, }),
            'description': forms.Textarea(attrs={'rows': 3, }),
            'comment': forms.Textarea(attrs={'rows': 5, })
        }


class RackAddForm(forms.ModelForm):
    name = forms.CharField(label='Rack Label', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="------", widget=forms.Select(attrs={'class': 'select2 form-control'}))
    u_height = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    desc_units = forms.BooleanField(label='Top to buttom', widget=forms.CheckboxInput(attrs={'class': 'form-control col-md-1'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Rack
        fields = ['name', 'location', 'u_height', 'desc_units', 'racktype', 'comment',
        ]
        widgets = {
            'racktype': StaticSelectWidget()
        }

