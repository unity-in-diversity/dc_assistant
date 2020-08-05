import django_tables2 as tables
#from extend.tables import BaseTable
from django_tables2.utils import Accessor
from .models import Location, Rack

SITE_REGION_LINK = """
{% if record.region %}
    <a href="{% url 'organisation:location_list' %}?region={{ record.region.slug }}">{{ record.region }}</a>
{% else %}
    &mdash;
{% endif %} 
"""

RACK_DEVICE_COUNT = """
<a href="{% url 'organisation:device_list' %}?rack_id={{ record.pk }}">{{ value }}</a>
"""

class LocationTable(tables.Table):
    name = tables.LinkColumn(order_by=('name',))
    region = tables.TemplateColumn(template_code=SITE_REGION_LINK)

    class Meta:
        model = Location
        fields = ('name', 'region', 'description')
        attrs = {'class': 'table'}
        #template_name = "django_tables2/bootstrap4.html"

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
        attrs = {'class': 'table'}
