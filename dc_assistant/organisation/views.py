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


def region_add(request):
    if request.method == 'POST':
        form = RegionAddForm(request.POST)
        if form.is_valid():
             new_region = Region(
                 parent=form.cleaned_data['parent'],
                 name=form.cleaned_data['name'],
                 slug=form.cleaned_data['slug'],
             )
             new_region.save()
             return HttpResponseRedirect(reverse('organisation:region_list'))
        else:
            form = RegionAddForm()
            return render(request, 'organisation/region_add.html', context={'form': form})
    else:
        form = RegionAddForm()
        return render(request, 'organisation/region_add.html', context={'form': form})

class LocationAdd(CreateView):
    form_class = SiteAddForm
    model = Location
    success_url = reverse_lazy('organisation:location_list')
    template_name = 'organisation/location_add.html'
