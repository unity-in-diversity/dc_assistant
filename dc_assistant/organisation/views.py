from django.shortcuts import render
from .forms import RegionAddForm
from .models import Region
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def region_view(request):
    regions = Region.objects.all()
    return render(request, 'organisation/regions.html', context={'regions': regions})

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