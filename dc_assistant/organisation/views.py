from django.shortcuts import render
from .forms import RegionAddForm, SiteAddForm
from .models import Region, Location
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, CreateView
# Create your views here.

def region_view(request):
    regions = Region.objects.all()
    return render(request, 'organisation/regions.html', context={'regions': regions})

def location_view(request):
    locations = Location.objects.all()
    return render(request, 'organisation/locations.html', context={'locations': locations})

class RegionAdd(CreateView):
    form_class = RegionAddForm
    model = Region
    success_url = reverse_lazy('organisation:region_list')
    template_name = 'organisation/region_add.html'

class LocationAdd(CreateView):
    form_class = SiteAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'
