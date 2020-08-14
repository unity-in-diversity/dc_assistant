from django.urls import path
from extend import views


app_name = 'extend'
urlpatterns = [

    path('tags/', views.TagListView.as_view(), name='tag_list'),
    ]