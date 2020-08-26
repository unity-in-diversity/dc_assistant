from django.views.generic import View
from django.contrib.auth.views import LoginView
from .forms import UserAuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.shortcuts import render, reverse
from django.utils.http import is_safe_url
from django.contrib import messages


class UserLoginView(LoginView):
    template_name = 'secret/login.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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


class SecretListView(View):
    pass