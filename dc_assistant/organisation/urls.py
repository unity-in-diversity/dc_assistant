from django.urls import path
from . import views
from dc_assistant import views as homeviews

app_name = 'organisation'

urlpatterns = [
    path('regions/', views.region_view, name='region_list'),
    path('regions/add', views.region_add, name='region_add'),
    path('locations/', homeviews.main_view, name='location_list'),
]
