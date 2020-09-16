"""dc_assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import MainView, APIRootView
from secret.views import UserLoginView, UserProfileView, UserChangePasswordView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from dc_assistant.admin import admin_site

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('admin/', admin_site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='secret/change_password_done.html'), name='change_password_done'),
    path('api/', APIRootView.as_view(), name='api-root'),
    path('api/secrets/', include('secret.api.urls')),
    path('api/organisation/', include('organisation.api.urls')),
    path('organisation/', include('organisation.urls')),
    path('extend/', include('extend.urls')),
    path('secret/', include('secret.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]