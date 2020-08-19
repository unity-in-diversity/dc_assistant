import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from organisation.models import Region, Location, Vendor, VendorModel, Rack
from extend.models import Tag

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
    Match on one or more assigned tags. If multiple tags are specified (e.g. ?tag=foo&tag=bar), the queryset is filtered
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