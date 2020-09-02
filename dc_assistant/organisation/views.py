from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView, UpdateView
from .forms import RegionAddForm, LocationAddForm, RackAddForm, VendorModelAddForm, RoleModelAddForm, DeviceAddForm, PlatformAddForm
from .models import Region, Location, Rack, VendorModel, Device, DeviceRole, Platform
from extend.views import ListObjectsView
from extend import filters
from .tables import RegionTable, LocationTable, RackTable, VendorModelTable, DeviceRoleTable, DeviceTable, PlatformTable


class RegionListView(PermissionRequiredMixin, ListObjectsView):
    permission_required = 'organisation.view_region'
    queryset = Region.objects.all()
    table = RegionTable
    template_name = 'organisation/region_tab.html'


class RegionAdd(CreateView):
    permission_required = 'organisation.edit_region'
    form_class = RegionAddForm
    model = Region
    success_url = reverse_lazy('organisation:region_list')
    template_name = 'organisation/region_add.html'


class RegionEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'organisation.change_region'
    model = Region
    form_class = RegionAddForm
    success_url = reverse_lazy('organisation:region_list')
    template_name = 'organisation/region_add.html'


class LocationListView(PermissionRequiredMixin, ListObjectsView):
    permission_required = 'organisation.view_location'
    queryset = Location.objects.prefetch_related('region')
    filterset = filters.LocationFilterSet
    table = LocationTable
    template_name = 'organisation/locations_tab.html'


class LocationAdd(CreateView):
    form_class = LocationAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'


class LocationEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'organisation.change_location'
    model = Location
    form_class = LocationAddForm
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'


class LocationView(PermissionRequiredMixin, View):
    permission_required = 'organisation.view_location'

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
    queryset = Rack.objects.prefetch_related('location').annotate(device_count=Count('devices'))
    filterset = filters.RackFilterSet
    table = RackTable
    template_name = 'organisation/racks_tab.html'


class RackAdd(CreateView):
    form_class = RackAddForm
    model = Rack
    success_url = reverse_lazy('organisation:rack_list')
    template_name = 'organisation/rack_add.html'


class RackView(View):

    def get(self, request, pk):

        rack = get_object_or_404(Rack.objects.prefetch_related('location__region'), pk=pk)
        nonracked_devices = Device.objects.filter(
            rack=rack,
            position__isnull=True,
        ).prefetch_related('device_model__vendor')
        return render(request, 'organisation/rack.html', {
            'rack': rack,
            'nonracked_devices': nonracked_devices,
        })


class VendorModelListView(ListObjectsView):
    queryset = VendorModel.objects.prefetch_related('vendor').annotate(instance_count=Count('instances'))
    filterset = filters.DeviceModelFilterSet
    table = VendorModelTable
    template_name = 'organisation/models_tab.html'


class VendorModelAdd(CreateView):
    form_class = VendorModelAddForm
    model = VendorModel
    success_url = reverse_lazy('organisation:model_list')
    template_name = 'organisation/model_add.html'


class PlatformListView(ListObjectsView):
    queryset = Platform.objects.all()
    table = PlatformTable
    template_name = 'organisation/platforms_tab.html'


class PlatformAdd(CreateView):
    form_class = PlatformAddForm
    model = Platform
    success_url = reverse_lazy('organisation:platform_list')
    template_name = 'organisation/platform_add.html'


class RoleDeviceListView(ListObjectsView):
    queryset = DeviceRole.objects.all()
    table = DeviceRoleTable
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


class DeviceListView(ListObjectsView):
    queryset = Device.objects.prefetch_related(
        'device_model__vendor', 'device_role', 'location', 'rack'
    )
    filterset = filters.DeviceFilterSet
    table = DeviceTable
    template_name = 'organisation/device_tab.html'


class DeviceView(View):

    def get(self, request, pk):

        device = get_object_or_404(Device.objects.prefetch_related(
            'location__region', 'device_role', 'platform'
        ), pk=pk)

        #services = device.services.all()
        #secrets = device.secrets.all()

        return render(request, 'organisation/device.html', {
            'device': device,
            #'services': services,
            #'secrets': secrets,
        })
