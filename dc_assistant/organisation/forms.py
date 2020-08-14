from django import forms
from mptt.forms import TreeNodeChoiceField
from taggit.forms import TagField
from django.forms import Textarea, TextInput, NumberInput
from .models import Region, Location, Rack, VendorModel, Vendor, DeviceRole, Device, Platform

class StaticSelectWidget(forms.Select):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'select2 form-control custom-select'

class SlugWidget(forms.TextInput):
    """
    Тип поля основанный на TextInput с доп. шаблоном для автоматического формирования значения поля с помощью JS скрипта.
    """
    template_name = 'sluginput.html'

class SlugField(forms.SlugField):
    """
    Расширение встроенного поля SlugField позволяет автоматически формировать значение
    поля исползуя значение поля `name` реализовано только для ENG.
    """
    def __init__(self, slug_source='name', *args, **kwargs):
        label = kwargs.pop('label', "Slug")
        #help_text = kwargs.pop('help_text', "URL-friendly")
        widget = kwargs.pop('widget', SlugWidget)
        super().__init__(label=label, widget=widget, *args, **kwargs)
        self.widget.attrs['slug-source'] = slug_source

class RegionAddForm(forms.ModelForm):
    parent = TreeNodeChoiceField(label='Родитель', required=False, queryset=Region.objects.all(), level_indicator = u'-', widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Название региона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #slug = forms.CharField(label='Псевдоним', widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = SlugField(slug_source='name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Region
        fields = (
            'parent', 'name', 'slug',
        )

class LocationAddForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = SlugField(slug_source='name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    region = TreeNodeChoiceField(
        label='Регион',
        queryset=Region.objects.all(),
        required=False,
        level_indicator=u'-',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    physical_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


    class Meta:
        model = Location
        fields = [
            'name', 'slug', 'region', 'physical_address', 'description', 'comment'
        ]
        widgets = {
            'physical_address': Textarea(attrs={'rows': 3, }),
            'description': Textarea(attrs={'rows': 3, }),
            'comment': Textarea(attrs={'rows': 5, })
        }


class RackAddForm(forms.ModelForm):
    name = forms.CharField(label='Rack Label', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="------", widget=forms.Select(attrs={'class': 'select2 form-control'}))
    u_height = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    desc_units = forms.BooleanField(label='Top to buttom', widget=forms.CheckboxInput(attrs={'class': 'form-control col-md-1'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Rack
        fields = ['name', 'location', 'u_height', 'desc_units', 'racktype', 'comment']
        widgets = {
            'racktype': StaticSelectWidget()
        }

class VendorModelAddForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), empty_label="------",
                                    widget=forms.Select(attrs={'class': 'select2 form-control'}))
    #slug = SlugField(slug_source='model')
    slug = SlugField(slug_source='model', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = VendorModel
        fields = ['model', 'vendor', 'slug', 'u_height', 'front_image', 'rear_image', 'comment']
        widgets = {
            'model': TextInput(attrs={'class': 'form-control'}),
            'u_height': NumberInput(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control', 'rows': 5,}),
        }

class RoleModelAddForm(forms.ModelForm):
    slug = SlugField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DeviceRole
        fields = ['name', 'slug', 'color', 'description',]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'select2 form-control custom-select select2-hidden-accessible'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        }

class DeviceAddForm(forms.ModelForm):
        site = forms.ModelChoiceField(
            queryset=Location.objects.all()
        )
        rack = forms.ModelChoiceField(
            queryset=Rack.objects.all(),
            required=False,
        )
        position = forms.TypedChoiceField(
            required=False,
            empty_value=None,
        )
        vendor = forms.ModelChoiceField(
            queryset=Vendor.objects.all(),
            required=False,
        )
        device_model = forms.ModelChoiceField(
            queryset=VendorModel.objects.all(),
        )
        device_role = forms.ModelChoiceField(
            queryset=DeviceRole.objects.all(),
        )
        platform = forms.ModelChoiceField(
            queryset=Platform.objects.all(),
            required=False,
        )
        tags = TagField(required=False)
        comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

        class Meta:
            model = Device
            fields = [
                'name', 'device_role', 'device_model', 'serial', 'location', 'rack', 'position', 'face',
                'platform', 'description', 'comments'
            ]
            widgets = {
                'face': StaticSelectWidget(),
            }
