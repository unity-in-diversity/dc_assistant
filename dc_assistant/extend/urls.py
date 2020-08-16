from django.urls import path, re_path

from extend import views
from .views import RackAutocomplete


app_name = 'extend'
urlpatterns = [

    path('tags/', views.TagListView.as_view(), name='tag_list'),
    re_path(r'^rack-autocomplete/$', RackAutocomplete.as_view(), name='rack-autocomplete'),
    ]