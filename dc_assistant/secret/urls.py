from django.urls import path
from . import views

app_name = 'secret'
urlpatterns = [
    path('secrets/', views.SecretListView.as_view(), name='secret_list'),
    ]
