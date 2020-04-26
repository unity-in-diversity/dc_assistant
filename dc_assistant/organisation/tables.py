import django_tables2 as tables
#from extend.tables import BaseTable
from .models import Location

SITE_REGION_LINK = """
{% if record.region %}
    <a href="{% url 'organisation:location_list' %}?region={{ record.region.slug }}">{{ record.region }}</a>
{% else %}
    &mdash;
{% endif %}
"""

class LocationTable(tables.Table):
    #pk = ToggleColumn()
    name = tables.LinkColumn(order_by=('name',))
    region = tables.TemplateColumn(template_code=SITE_REGION_LINK)

    class Meta:
        model = Location
        fields = ('name', 'region', 'description')
        #fields = ('pk', 'name', 'region', 'description')
        attrs = {'class': 'table table-hover table-headings'}