from django import forms
from taggit.forms import TagField
from django.forms import TextInput
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from .models import Secret, UserKey


def validate_rsa_key(key, is_secret=True):
    """
    Validate the format and type of an RSA key.
    """
    if key.startswith('ssh-rsa '):
        raise forms.ValidationError("OpenSSH line format is not supported. Please ensure that your public is in PEM (base64) format.")
    try:
        key = RSA.importKey(key)
    except ValueError:
        raise forms.ValidationError("Invalid RSA key. Please ensure that your key is in PEM (base64) format.")
    except Exception as e:
        raise forms.ValidationError("Invalid key detected: {}".format(e))
    if is_secret and not key.has_private():
        raise forms.ValidationError("This looks like a public key. Please provide your private RSA key.")
    elif not is_secret and key.has_private():
        raise forms.ValidationError("This looks like a private key. Please provide your public RSA key.")
    try:
        PKCS1_OAEP.new(key)
    except Exception:
        raise forms.ValidationError("Error validating RSA key. Please ensure that your key supports PKCS#1 OAEP.")


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

class UserKeyAddForm(forms.ModelForm):

    class Meta:
        model = UserKey
        fields = ['public_key']
        help_texts = {
            'public_key': "Enter your public RSA key. Keep the private, save to file or notes. "
                          "You'll need it for decryption. Privat key like passphrase!",
        }
        labels = {
            'public_key': ''
        }

    def clean_public_key(self):
        key = self.cleaned_data['public_key']

        # Validate the RSA key format.
        validate_rsa_key(key, is_secret=False)

        return key

class SecretAddForm(forms.BaseForm):
    plaintext = forms.CharField(
        max_length=65535,
        required=False,
        label='Plaintext',
        widget=forms.PasswordInput(
            attrs={
                'class': 'requires-session-key',
            }
        )
    )
    plaintext2 = forms.CharField(
        max_length=65535,
        required=False,
        label='Plaintext (verify)',
        widget=forms.PasswordInput()
    )
    tag = TagField(
        required=False,
        help_text="Вводить через запятую",
        widget=TextInput(attrs={'data-role': 'tagsinput'}))

    class Meta:
        model = Secret
        fields = [
            'name', 'role', 'plaintext', 'plaintext2', 'tag',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # A plaintext value is required when creating a new Secret
        if not self.instance.pk:
            self.fields['plaintext'].required = True

    def clean(self):

        # Verify that the provided plaintext values match
        if self.cleaned_data['plaintext'] != self.cleaned_data['plaintext2']:
            raise forms.ValidationError({
                'plaintext2': "Secrets(passwords) do not match. Please check input try again."
            })
