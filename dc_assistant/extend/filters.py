import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from organisation.models import Region, Location, Vendor, VendorModel, Rack, DeviceRole, Platform, Device
from extend.models import Tag
from secret.models import Secret, SecretRole

__all__ = (
    'LocationFilterSet',
    'RackFilterSet',
    'DeviceModelFilterSet',
    'DeviceFilterSet',
    'SecretFilterSet',
)


class NumericInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    Filters for set of numeric values. Example: id__in=100,200,300
    """
    pass


class TreeNodeMultipleChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    """
    Filters for a set of Models, including all descendant models within a Tree.  Example: [<Region: R1>,<Region: R2>]
    """

    def get_filter_predicate(self, v):
        # null value filtering
        if v is None:
            return {self.field_name.replace('in', 'isnull'): True}
        return super().get_filter_predicate(v)

    def filter(self, qs, value):
        value = [node.get_descendants(include_self=True) if not isinstance(node, str) else node for node in value]
        return super().filter(qs, value)

class TagFilter(django_filters.ModelMultipleChoiceFilter):
    """
    Match one or more tags. If two and more tags (?tag=onetag&tag=secondtag), the queryset is filtered
    to objects matching all tags.
    """
    def __init__(self, *args, **kwargs):

        kwargs.setdefault('field_name', 'tag__slug')
        kwargs.setdefault('to_field_name', 'slug')
        kwargs.setdefault('conjoined', True)
        kwargs.setdefault('queryset', Tag.objects.all())

        super().__init__(*args, **kwargs)


class LocationFilterSet(django_filters.FilterSet):
    # region_id = TreeNodeMultipleChoiceFilter(
    #     queryset=Region.objects.all(),
    #     field_name='region__in',
    #     label='Region (ID)',
    # )
    region = TreeNodeMultipleChoiceFilter(
        queryset=Region.objects.all(),
        field_name='region__in',
        to_field_name='slug',
        label='Region (slug)',
    )
    tag = TagFilter()

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'slug',
        ]


class RackFilterSet(django_filters.FilterSet):
    location = django_filters.ModelMultipleChoiceFilter(
        field_name='location__slug',
        queryset=Location.objects.all(),
        to_field_name='slug',
        label='Site (slug)',
    )
    class Meta:
        model = Rack
        fields = [
            'id', 'name', 'racktype', 'u_height'
        ]

class DeviceModelFilterSet(django_filters.FilterSet):
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Vendor.objects.all(),
        label='Vendor (ID)',
    )
    vendor = django_filters.ModelMultipleChoiceFilter(
        field_name='vendor__slug',
        queryset=Vendor.objects.all(),
        to_field_name='slug',
        label='Vendor (slug)',
    )

    class Meta:
        model = VendorModel
        fields = [
            'model', 'slug',
        ]

class DeviceFilterSet(django_filters.FilterSet):

    rack_id = django_filters.ModelMultipleChoiceFilter(
        field_name='rack',
        queryset=Rack.objects.all(),
        label='Rack (ID)',
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='device_role__slug',
        queryset=DeviceRole.objects.all(),
        to_field_name='slug',
        label='Role (slug)',
    )
    device_model_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VendorModel.objects.all(),
        label='Device type (ID)',
    )
    vendor_id = django_filters.ModelMultipleChoiceFilter(
        field_name='device_model__vendor',
        queryset=Vendor.objects.all(),
        label='Manufacturer (ID)',
    )
    platform = django_filters.ModelMultipleChoiceFilter(
        field_name='platform__slug',
        queryset=Platform.objects.all(),
        to_field_name='slug',
        label='Platform (slug)',
    )


class SecretFilterSet(django_filters.FilterSet):
    id__in = NumericInFilter(
        field_name='id',
        lookup_expr='in'
    )
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    role_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecretRole.objects.all(),
        label='Role (ID)',
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='role__slug',
        queryset=SecretRole.objects.all(),
        to_field_name='slug',
        label='Role (slug)',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )
    tag = TagFilter()

    class Meta:
        model = Secret
        fields = ['name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(device__name__icontains=value)
        )
