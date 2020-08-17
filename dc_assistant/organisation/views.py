from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
#from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView, ListView
from .forms import RegionAddForm, LocationAddForm, RackAddForm, VendorModelAddForm, RoleModelAddForm, DeviceAddForm
from .models import Region, Location, Rack, VendorModel, Device, DeviceRole
from extend.views import ListObjectsView
from extend import filters
from .tables import LocationTable, RackTable, VendorModelTable, DeviceRoleTable
#from django_tables2 import RequestConfig
from django_tables2 import SingleTableView
from django_tables2 import LazyPaginator

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
    table = LocationTable
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/locations_tab.html'


class LocationAdd(CreateView):
    form_class = LocationAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'

class LocationView(View):

    def get(self, request, slug):
        location = get_object_or_404(Location.objects.prefetch_related('region'), slug=slug)
        stats = {
            'rack_count': Rack.objects.filter(location=location).count(),
            'device_count': Device.objects.filter(location=location).count(),
        }

        return render(request, 'organisation/location.html', {
            'location': location,
            'stats': stats,
        })


class RackListView(ListObjectsView):
    #queryset = Rack.objects.all()
    queryset = Rack.objects.prefetch_related('location').annotate(device_count=Count('devices'))
    #table_class = RackTable
    filterset = filters.RackFilterSet
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

class VendorModelListView(ListObjectsView):
    queryset = VendorModel.objects.prefetch_related('vendor').annotate(instance_count=Count('instances'))
    filterset = filters.DeviceModelFilterSet
    # table_class = RackTable
    table = VendorModelTable
    success_url = reverse_lazy('organisation:model_list')
    template_name = 'organisation/models_tab.html'

class VendorModelAdd(CreateView):
    form_class = VendorModelAddForm
    model = VendorModel
    success_url = reverse_lazy('organisation:model_list')
    template_name = 'organisation/model_add.html'

# class VendorModelView(View):
#     pass

class RoleDeviceListView(ListObjectsView):
    queryset = DeviceRole.objects.all()
    table = DeviceRoleTable
    success_url = reverse_lazy('organisation:role_list')
    template_name = 'organisation/roles_tab.html'

class RoleDeviceAdd(CreateView):
    form_class = RoleModelAddForm
    model = DeviceRole
    success_url = reverse_lazy('organisation:role_list')
    template_name = 'organisation/role_add.html'

class DeviceAdd(CreateView):
    form_class = DeviceAddForm
    model = Device
    success_url = reverse_lazy('organisation:device_list')
    template_name = 'organisation/device_add.html'
    pass

class DeviceListView(ListObjectsView):
    queryset = DeviceRole.objects.all()
    table = DeviceRoleTable
    success_url = reverse_lazy('organisation:role_list')
    template_name = 'organisation/device_tab.html'

class DeviceView(View):
    pass