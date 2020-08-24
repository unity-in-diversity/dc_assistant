from django.urls import path
from . import views
from dc_assistant import views as homeviews

app_name = 'organisation'

urlpatterns = [
    path('regions/', views.region_list_view, name='region_list'),
    path('regions/add', views.RegionAdd.as_view(), name='region_add'),

    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/add', views.LocationAdd.as_view(), name='location_add'),
    path('locations/<slug:slug>/', views.LocationView.as_view(), name='location'),

    path('racks/', views.RackListView.as_view(), name='rack_list'),
    path('racks/add', views.RackAdd.as_view(), name='rack_add'),
    path('racks/<int:pk>/', views.RackView.as_view(), name='rack'),

    path('models/', views.VendorModelListView.as_view(), name='model_list'),
    path('models/add', views.VendorModelAdd.as_view(), name='model_add'),

    path('roles/', views.RoleDeviceListView.as_view(), name='role_list'),
    path('roles/add', views.RoleDeviceAdd.as_view(), name='role_add'),

    path('platforms/', views.PlatformListView.as_view(), name='platform_list'),
    path('platforms/add', views.PlatformAdd.as_view(), name='platfrom_add'),

    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('devices/add', views.DeviceAdd.as_view(), name='device_add'),
    path('devices/<int:pk>/', views.DeviceView.as_view(), name='device'),

]
