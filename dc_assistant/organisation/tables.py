import django_tables2 as tables
#from extend.tables import BaseTable
from django_tables2.utils import Accessor
from .models import Region, Location, Rack, VendorModel, DeviceRole, Device, Platform


REGION_ACTIONS = """
    <a href="{% url 'organisation:region_edit' pk=record.pk %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

LOCATION_ACTIONS = """
    <a href="{% url 'organisation:location_edit' slug=record.slug %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

LOCATION_REGION_LINK = """
{% if record.region %}
    <a href="{% url 'organisation:location_list' %}?region={{ record.region.slug }}">{{ record.region }}</a>
{% else %}
    &mdash;
{% endif %} 
"""

RACK_DEVICE_COUNT = """
<a href="{% url 'organisation:device_list' %}?rack_id={{ record.pk }}">{{ value }}</a>
"""

DEVICEMODEL_INSTANCES_TEMPLATE = """
<a href="{% url 'organisation:device_list' %}?vendor_id={{ record.vendor_id }}&device_model_id={{ record.pk }}">{{ record.instance_count }}</a>
"""

DEVICEMODEL_ACTIONS = """
<a href="{% url 'organisation:model_edit' pk=record.pk %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

VENDOR_ACTIONS = """
<a href="{% url 'organisation:vendor_edit' pk=record.pk %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

PLATFORM_DEVICE_COUNT = """
<a href="{% url 'organisation:device_list' %}?platform={{ record.slug }}">{{ value }}</a>
"""

PLATFORM_ACTIONS = """
<a href="{% url 'organisation:platform_edit' slug=record.slug %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

DEVICEROLE_DEVICE_COUNT = """
<a href="{% url 'organisation:device_list' %}?role={{ record.slug }}">{{ value }}</a>
"""

DEVICEROLE_ACTIONS = """
<a href="{% url 'organisation:role_edit' pk=record.pk %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""

DEVICE_LINK = """
<a href="{% url 'organisation:device' pk=record.pk %}">
    {{ record.name|default:'<span class="label label-info">Unnamed device</span>' }}
</a>
"""

DEVICE_ROLE = """
{% load utils %}
<label class="label" style="color: {{ record.device_role.color|fgcolor }}; background-color: #{{ record.device_role.color }}">{{ value }}</label>
"""

COLOR_LABEL = """
{% load utils %}
<label class="label" style="color: {{ record.color|fgcolor }}; background-color: #{{ record.color }}">{{ record }}</label>
"""



class RegionTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code=REGION_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = Region
        fields = ('name', 'parent', 'slug', 'actions')
        attrs = {'class': 'table table-hover table-headings'}

class LocationTable(tables.Table):
    name = tables.LinkColumn(order_by=('name',))
    region = tables.TemplateColumn(template_code=LOCATION_REGION_LINK)
    actions = tables.TemplateColumn(
        template_code=LOCATION_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = Location
        fields = ('name', 'region', 'description', 'actions')
        attrs = {'class': 'table table-hover table-headings'}

class RackTable(tables.Table):
    name = tables.LinkColumn(order_by=('name',))
    location = tables.LinkColumn('organisation:location', args=[Accessor('location.slug')])
    u_height = tables.TemplateColumn("{{ record.u_height }}U", verbose_name='Height')
    device_count = tables.TemplateColumn(
        template_code=RACK_DEVICE_COUNT,
        verbose_name='Devices'
    )


    class Meta:
        model = Rack
        fields = ('name', 'location', 'u_height', 'device_count')
        attrs = {'class': 'table table-hover table-headings',}

class VendorModelTable(tables.Table):
    #model = tables.LinkColumn('organisation:model', args=[Accessor('pk')], verbose_name='Device Model')
    instance_count = tables.TemplateColumn(
        template_code=DEVICEMODEL_INSTANCES_TEMPLATE,
        verbose_name='Instances')
    actions = tables.TemplateColumn(
        template_code=DEVICEMODEL_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = VendorModel
        fields = ('model', 'vendor', 'u_height', 'depth', 'instance_count' 'actions')
        attrs = {'class': 'table table-hover table-headings',}

class DeviceRoleTable(tables.Table):
    device_count = tables.TemplateColumn(
        template_code=DEVICEROLE_DEVICE_COUNT,
        accessor=Accessor('devices.count'),
        orderable=False,
        verbose_name='Devices'
    )
    color = tables.TemplateColumn(COLOR_LABEL, verbose_name='Label')
    # slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(
        template_code=DEVICEROLE_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = DeviceRole
        fields = ('name', 'device_count', 'color', 'description', 'actions')
        attrs = {'class': 'table table-hover table-headings', }

class DeviceTable(tables.Table):
    name = tables.TemplateColumn(
        order_by=('name',),
        template_code=DEVICE_LINK
    )
    location = tables.LinkColumn('organisation:location', args=[Accessor('location.slug')])
    rack = tables.LinkColumn('organisation:rack', args=[Accessor('rack.pk')])
    device_role = tables.TemplateColumn(DEVICE_ROLE, verbose_name='Role')
    # device_model = tables.LinkColumn(
    #     'organisation:vendormodel', args=[Accessor('device_model.pk')], verbose_name='Model',
    #     text=lambda record: record.device_model.display_name
    # )

    class Meta:
        model = Device
        fields = ('name', 'platform', 'device_role', 'device_model', 'location', 'rack',)
        attrs = {'class': 'table table-hover table-headings', }

class PlatformTable(tables.Table):
    device_count = tables.TemplateColumn(
        template_code=PLATFORM_DEVICE_COUNT,
        accessor=Accessor('devices.count'),
        orderable=False,
        verbose_name='Devices'
    )
    actions = tables.TemplateColumn(
        template_code=PLATFORM_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = Platform
        fields = ('name', 'slug', 'device_count', 'actions')
        attrs = {'class': 'table table-hover table-headings', }


class VendorTable(tables.Table):
    actions = tables.TemplateColumn(
        template_code=VENDOR_ACTIONS,
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta:
        model = Platform
        fields = ('name', 'slug', 'actions')
        attrs = {'class': 'table table-hover table-headings', }
