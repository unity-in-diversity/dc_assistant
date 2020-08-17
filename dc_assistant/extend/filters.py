import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from organisation.models import Region, Location, Vendor, VendorModel, Rack

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
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'slug',
        ]

    # def search(self, queryset, name, value):
    #     if not value.strip():
    #         return queryset
    #     qs_filter = (
    #         Q(name__icontains=value) |
    #         Q(facility__icontains=value) |
    #         Q(description__icontains=value) |
    #         Q(physical_address__icontains=value) |
    #         Q(shipping_address__icontains=value) |
    #         Q(contact_name__icontains=value) |
    #         Q(contact_phone__icontains=value) |
    #         Q(contact_email__icontains=value) |
    #         Q(comments__icontains=value)
    #     )
    #     try:
    #         qs_filter |= Q(asn=int(value.strip()))
    #     except ValueError:
    #         pass
    #     return queryset.filter(qs_filter)

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