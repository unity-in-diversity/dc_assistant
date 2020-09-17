from dal import autocomplete
from django import forms
from mptt.forms import TreeNodeChoiceField
from taggit.forms import TagField
from django.forms import Textarea, TextInput, NumberInput
from .models import Region, Location, Rack, VendorModel, Vendor, DeviceRole, Device, Platform
from extend.forms import StaticSelectWidget, SlugField


class RegionAddForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        label='Parent',
        required=False,
        queryset=Region.objects.all(),
        level_indicator = u'-',
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    name = forms.CharField(
        label='Region Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    slug = SlugField(
        slug_source='name',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Region
        fields = (
            'parent', 'name', 'slug',
        )

class LocationAddForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    slug = SlugField(
        slug_source='name',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    region = TreeNodeChoiceField(
        label='Region',
        queryset=Region.objects.all(),
        required=False,
        level_indicator=u'-',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    physical_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        })
    )

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
    name = forms.CharField(
        label='Rack Label',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label="------",
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    u_height = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )
    #desc_units = forms.BooleanField(label='Top to buttom', widget=forms.CheckboxInput(attrs={'class': 'form-control col-md-1'}))
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Rack
        fields = ['name', 'location', 'u_height', 'desc_units', 'racktype', 'comment']
        widgets = {
            'racktype': StaticSelectWidget(),
            'desc_units': StaticSelectWidget()
        }


class VendorModelAddForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.all(),
        empty_label="------",
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    slug = SlugField(
        slug_source='model',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    class Meta:
        model = VendorModel
        fields = ['model', 'vendor', 'slug', 'u_height', 'front_image', 'rear_image', 'comment']
        widgets = {
            'model': TextInput(attrs={'class': 'form-control'}),
            'u_height': NumberInput(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={'class': 'form-control', 'rows': 5,}),
        }


class RoleModelAddForm(forms.ModelForm):
    slug = SlugField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = DeviceRole
        fields = ['name', 'slug', 'color', 'description',]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'select2 form-control custom-select select2-hidden-accessible'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 5, }),
        }


class PlatformAddForm(forms.ModelForm):
    slug = SlugField(
        slug_source='name',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Platform
        fields = ['name', 'slug',]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class VendorAddForm(forms.ModelForm):
    slug = SlugField(
        slug_source='name',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Vendor
        fields = ['name', 'slug',]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class DeviceAddForm(forms.ModelForm):
    error_css_class = 'error'

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    device_model = forms.ModelChoiceField(
        queryset=VendorModel.objects.all(),
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    tag = TagField(
        required=False,
        help_text="separated by commas",
        widget=TextInput(attrs={
            'data-role': 'tagsinput'
        })
    )

    class Meta:
        model = Device
        fields = [
            'name', 'device_role', 'device_model', 'serial', 'location', 'rack', 'position', 'face_position',
            'platform', 'description', 'comment', 'tag',
            ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'device_role': forms.Select(attrs={'class': 'select2 form-control custom-select'}),
            'device_model': forms.Select(attrs={'class': 'select2 form-control custom-select'}),
            'serial': TextInput(attrs={'class': 'form-control'}),
            'rack': autocomplete.ModelSelect2(url='extend:rack_autocomplete', forward=['location']),
            'position': NumberInput(attrs={'class': 'form-control'}),
            'face_position': StaticSelectWidget(),
            'platform': forms.Select(attrs={'class': 'select2 form-control custom-select'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 5, }),
            'comment': Textarea(attrs={'class': 'form-control', 'rows': 5, })

        }

    class Media:
        js = (
            'linked_data.js',
        )
