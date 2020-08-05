from django.shortcuts import render
from django.db.models import Count
#from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView, ListView
from .forms import RegionAddForm, LocationAddForm, RackAddForm
from .models import Region, Location, Rack
from extend.views import ListObjectsView
from extend import filters
from .tables import LocationTable, RackTable
#from django_tables2 import RequestConfig
from django_tables2 import SingleTableView


def region_list_view(request):
    regions = Region.objects.all()
    return render(request, 'organisation/regions.html', context={'regions': regions})

class RegionAdd(CreateView):
    form_class = RegionAddForm
    model = Region
    success_url = reverse_lazy('organisation:region_list')
    template_name = 'organisation/region_add.html'


class LocationListView(ListObjectsView):
    #permission_required = 'dcim.view_site'
    #queryset = Location.objects.all()
    queryset = Location.objects.prefetch_related('region')
    filterset = filters.LocationFilterSet
    #model = Location
    table = LocationTable
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/locations_tab.html'


class LocationAdd(CreateView):
    form_class = LocationAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'

class LocationView(View):
    pass


class RackListView(ListObjectsView):
    #queryset = Rack.objects.all()
    queryset = Rack.objects.prefetch_related('location').annotate(device_count=Count('devices'))
    #table_class = RackTable
    table = RackTable
    success_url = reverse_lazy('organisation:rack_list')
    template_name = 'organisation/racks_tab.html'

class RackAdd(CreateView):
    form_class = RackAddForm
    model = Rack
    success_url = reverse_lazy('organisation:rack_list')
    template_name = 'organisation/rack_add.html'

class RackView(View):
    pass

class DeviceListView(View):
    pass

class DeviceView(View):
    pass
