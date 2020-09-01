from django.views.generic import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import UserAuthenticationForm, UserChangePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.shortcuts import render, reverse, redirect
from django.utils.http import is_safe_url
from django.contrib import messages
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'secret/login.html'

    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = UserAuthenticationForm(request)

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):

        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            redirect_to = request.POST.get('next', '')
            print(redirect_to)
            if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
                redirect_to = reverse('home')
            auth_login(request, form.get_user())
            messages.info(request, "Logged in as {}.".format(request.user))
            return HttpResponseRedirect(redirect_to)

        return render(request, self.template_name, {
            'form': form,
        })


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'secret/change_password.html'
    form_class = UserChangePasswordForm
    success_url = reverse_lazy('change_password_done')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'secret/profile.html'

    def get(self, request):
        return render(request, self.template_name)

class SecretListView(View):
    pass