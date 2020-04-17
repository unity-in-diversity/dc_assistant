from django.urls import path
from . import views
from dc_assistant import views as homeviews

app_name = 'organisation'

urlpatterns = [
    path('regions/', views.region_view, name='region_list'),
    path('regions/add', views.region_add, name='region_add'),
    path('locations/', views.location_view, name='location_list'),
    path ('locations/add', views.LocationAdd.as_view(), name='location_add')
]
