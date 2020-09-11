import base64

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.http import is_safe_url
from django.contrib import messages
from django.urls import reverse_lazy

from organisation.models import Device
from extend.views import ListObjectsView
from .forms import UserAuthenticationForm, UserChangePasswordForm
from .models import SessionKey, Secret, UserKey
from .forms import SecretAddForm, UserKeyForm
from .decorators import userkey_required
from extend import filters
from .tables import SecretTable

class UserLoginView(LoginView):
    template_name = 'secret/login.html'

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


def get_session_key(request):
    """
    Extract and decode the session key from request.
    """
    session_key = request.COOKIES.get('session_key', None)
    if session_key is not None:
        return base64.b64decode(session_key)
    return session_key

@userkey_required()
def secret_add(request, pk):

    # Retrieve device
    device = get_object_or_404(Device, pk=pk)
    print('def secret_add begin device', device)
    secret = Secret(device=device)
    print('def secret_add begin secret', secret)
    session_key = get_session_key(request)

    if request.method == 'POST':
        form = SecretAddForm(request.POST, instance=secret)
        if form.is_valid():
            # Valid session key in order to create a Secret
            if session_key is None:
                form.add_error(None, "No session key was provided with the request. Unable to encrypt secret data.")
            # Create and encrypt the new Secret
            else:
                master_key = None
                try:
                    sk = SessionKey.objects.get(userkey__user=request.user)
                    print('sk:', sk)
                    master_key = sk.get_master_key(session_key)
                    print('master_key:', master_key)
                except SessionKey.DoesNotExist:
                    form.add_error(None, "No session key found for this user.")

                if master_key is not None:
                    secret = form.save(commit=False)
                    secret.plaintext = str(form.cleaned_data['plaintext'])
                    secret.encrypt(master_key)
                    secret.save()
                    form.save_m2m()
                    messages.success(request, "Added new secret: {}.".format(secret))

                    return redirect('organisation:device', pk=device.pk)

    else:
        form = SecretAddForm(instance=secret)

    return render(request, 'secret/secret_add_edit.html', {
        'secret': secret,
        'form': form,
        'return_url': device.get_absolute_url(),
    })

class UserKeyView(LoginRequiredMixin, View):
    template_name = 'secret/userkey.html'

    def get(self, request):
        try:
            userkey = UserKey.objects.get(user=request.user)
        except UserKey.DoesNotExist:
            userkey = None

        return render(request, self.template_name, {
            'userkey': userkey,
        })

class UserKeyAddEditView(LoginRequiredMixin, View):
    template_name = 'secret/userkey_add_edit.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.userkey = UserKey.objects.get(user=request.user)
        except UserKey.DoesNotExist:
            self.userkey = UserKey(user=request.user)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserKeyForm(instance=self.userkey)

        return render(request, self.template_name, {
            'userkey': self.userkey,
            'form': form,
        })

    def post(self, request):
        form = UserKeyForm(data=request.POST, instance=self.userkey)
        if form.is_valid():
            uk = form.save(commit=False)
            uk.user = request.user
            uk.save()
            messages.success(request, "Your user key is saved.")
            return redirect('secret:userkey')

        return render(request, self.template_name, {
            'userkey': self.userkey,
            'form': form,
        })

class SecretListView(PermissionRequiredMixin, ListObjectsView):
    permission_required = 'secret.view_secret'
    queryset = Secret.objects.prefetch_related('role', 'device')
    filterset = filters.SecretFilterSet
    table = SecretTable
    template_name = 'secret/secret_tab.html'

class SecretView(PermissionRequiredMixin, View):
    permission_required = 'secret.view_secret'

    def get(self, request, pk):

        secret = get_object_or_404(Secret, pk=pk)

        return render(request, 'secret/secret.html', {
            'secret': secret,
        })