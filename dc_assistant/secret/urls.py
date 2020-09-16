from django.urls import path
from . import views

app_name = 'secret'

urlpatterns = [
    path('user-key/', views.UserKeyView.as_view(), name='userkey'),
    path('user-key/edit/', views.UserKeyAddEditView.as_view(), name='userkey_edit'),
    path('secrets/', views.SecretListView.as_view(), name='secret_list'),
    path('secrets/<int:pk>/', views.SecretView.as_view(), name='secret'),

    path('secret-roles/', views.SecretRoleListView.as_view(), name='secretrole_list'),
    path('secret-roles/add/', views.SecretRoleAdd.as_view(), name='secretrole_add'),
    path('secret-roles/<slug:slug>/edit/', views.SecretRoleEdit.as_view(), name='secretrole_edit'),
    ]
