from django.shortcuts import render
from django.db.models import Count
from .forms import RegionAddForm, LocationAddForm, RackAddForm
from .models import Region, Location, Rack
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView, ListView
from . import tables

from django_tables2 import SingleTableView
from .tables import LocationTable, RackTable
# Create your views here.

def region_list_view(request):
    regions = Region.objects.all()
    return render(request, 'organisation/regions.html', context={'regions': regions})

class RegionAdd(CreateView):
    form_class = RegionAddForm
    model = Region
    success_url = reverse_lazy('organisation:region_list')
    template_name = 'organisation/region_add.html'

# def location_view(request):
#     locations = Location.objects.all()
#     return render(request, 'organisation/x_locations.html', context={'locations': locations})

class LocationListView(SingleTableView):
    #permission_required = 'dcim.view_site'
    queryset = Location.objects.all()
    #filterset = filters.SiteFilterSet
    #filterset_form = forms.SiteFilterForm
    #model = Location
    table_class = LocationTable
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/locations_tab.html'

class LocationAdd(CreateView):
    form_class = LocationAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'

class LocationView(View):
    pass

class RackListView(SingleTableView):
    #queryset = Rack.objects.all()
    queryset = Rack.objects.prefetch_related('location').annotate(device_count=Count('devices'))
    table_class = RackTable
    success_url = reverse_lazy('organisation:rack_list')
    template_name = 'organisation/rack_tab.html'

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
