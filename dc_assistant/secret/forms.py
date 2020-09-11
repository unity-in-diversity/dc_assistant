from django import forms
from django.forms import Textarea
from taggit.forms import TagField
from django.forms import TextInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from .models import Secret, UserKey, SecretRole


def validate_rsa_key(key, is_secret=True):
    """
    Validate format and type key pair.
    """
    if key.startswith('ssh-rsa '):
        raise forms.ValidationError("OpenSSH format is not supported. You need PEM (base64) format.")
    try:
        key = RSA.importKey(key)
    except ValueError:
        raise forms.ValidationError("Invalid RSA key.  You need PEM (base64) format.")
    except Exception as e:
        raise forms.ValidationError("Invalid key: {}".format(e))
    if is_secret and not key.has_private():
        raise forms.ValidationError("This looks like a public key. It needs your private key.")
    elif not is_secret and key.has_private():
        raise forms.ValidationError("This looks like a private key. Please provide your public key.")
    try:
        PKCS1_OAEP.new(key)
    except Exception:
        raise forms.ValidationError("Error validating key. Please ensure that your key valid.")


class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['aria-describedby'] = 'basic-addon1'

        self.fields['password'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].widget.attrs['aria-describedby'] = 'basic-addon2'


class UserChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'You current password'

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'New password again to confirm'


class UserKeyForm(forms.ModelForm):

    class Meta:
        model = UserKey
        fields = ['public_key']
        help_texts = {
            'public_key': "Enter your public key. Keep the private, save to file or notes. "
                          "You'll need it for decryption. Privat key like passphrase!",
        }
        labels = {
            'public_key': ''
        }
        widgets = {
            'public_key': Textarea(attrs={'class': 'form-control', 'rows': 12, })
        }

    def clean_public_key(self):
        key = self.cleaned_data['public_key']

        # Validate the key format.
        validate_rsa_key(key, is_secret=False)

        return key


class ActivateUserKeyForm(forms.Form):
    _selected_action = forms.ModelMultipleChoiceField(
        queryset=UserKey.objects.all(),
        label='User Keys'
    )
    secret_key = forms.CharField(
        label='Your private key',
        widget=forms.Textarea(attrs={
            'class': 'vLargeTextField'
        })
    )


class SecretAddForm(forms.ModelForm):
    plaintext = forms.CharField(
        max_length=65535,
        required=False,
        label='Plaintext',
        help_text="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'requires-session-key form-control'
        })
    )
    plaintext2 = forms.CharField(
        max_length=65535,
        required=False,
        label='Plaintext (verify)',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    role = forms.ModelChoiceField(
        queryset=SecretRole.objects.all(),
        empty_label="------",
        widget=forms.Select(attrs={
            'class': 'select2 form-control custom-select'
        })
    )
    tag = TagField(
        required=False,
        label='Tags',
        help_text="Вводить через запятую",
        widget=TextInput(attrs={
            'data-role': 'tagsinput'
        })
    )

    class Meta:
        model = Secret
        fields = [
            'name', 'role', 'plaintext', 'plaintext2', 'tag',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # A plaintext value is required when creating a new Secret
        if not self.instance.pk:
            self.fields['plaintext'].required = True

    def clean(self):
        # Verify that the provided plaintext values match
        if self.cleaned_data['plaintext'] != self.cleaned_data['plaintext2']:
            raise forms.ValidationError({
                'plaintext2': "Secrets(passwords) do not match. Please check input, try again."
            })
