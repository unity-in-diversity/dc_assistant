import base64
from rest_framework import routers
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from Crypto.PublicKey import RSA
from rest_framework.response import Response

from django.http import HttpResponseBadRequest
from secret.models import UserKey, SessionKey

ERR_USERKEY_MISSING = "No UserKey found for the current user."
ERR_USERKEY_INACTIVE = "UserKey has not been activated for decryption."
ERR_PRIVKEY_MISSING = "Private key was not provided."
ERR_PRIVKEY_INVALID = "Invalid private key."


class SecretsRootView(routers.APIRootView):
    """
    Secrets API root view
    """
    def get_view_name(self):
        return 'Secrets'


class GenerateRSAKeyPairViewSet(ViewSet):
    """
    Generate a new RSA key pair. The keys are returned in PEM format.
        {
            "public_key": "<public key>",
            "private_key": "<private key>"
        }
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):

        # Determine what size key to generate
        key_size = request.GET.get('key_size', 2048)
        if key_size not in range(2048, 4097, 256):
            key_size = 2048

        # Export RSA private and public keys in PEM format
        key = RSA.generate(key_size)
        private_key = key.exportKey('PEM')
        public_key = key.publickey().exportKey('PEM')

        return Response({
            'private_key': private_key,
            'public_key': public_key,
        })

class GetSessionKeyViewSet(ViewSet):
    """
    Retrieve a temporary session key to use for encrypting and decrypting secrets via the API. The user's private RSA
    key is POSTed with the name `private_key`.
    For example:

        curl -v -X POST -H "Authorization: Token <token>" -H "Accept: application/json; indent=4" \\
        --data-urlencode "private_key@<filename>" https://dcassistant/api/secrets/get-session-key/

    This request will yield a base64-encoded session key to be included in an `X-Session-Key` header in future requests:

        {
            "session_key": "+8t4SI6XikgVmB5+/urhozx9O5qCQANyOk1MNe6taRf="
        }

    This endpoint accepts one optional parameter: `preserve_key`. If True and a session key exists, the existing session
    key will be returned instead of a new one.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):

        # Read private key
        private_key = request.POST.get('private_key', None)
        if private_key is None:
            return HttpResponseBadRequest(ERR_PRIVKEY_MISSING)

        # Validate user key
        try:
            user_key = UserKey.objects.get(user=request.user)
        except UserKey.DoesNotExist:
            return HttpResponseBadRequest(ERR_USERKEY_MISSING)
        if not user_key.is_active():
            return HttpResponseBadRequest(ERR_USERKEY_INACTIVE)

        # Validate private key
        master_key = user_key.get_master_key(private_key)
        if master_key is None:
            return HttpResponseBadRequest(ERR_PRIVKEY_INVALID)

        try:
            current_session_key = SessionKey.objects.get(userkey__user_id=request.user.pk)
        except SessionKey.DoesNotExist:
            current_session_key = None

        if current_session_key and request.GET.get('preserve_key', False):

            # Retrieve the existing session key
            key = current_session_key.get_session_key(master_key)

        else:

            # Create a new SessionKey
            SessionKey.objects.filter(userkey__user=request.user).delete()
            sk = SessionKey(userkey=user_key)
            sk.save(master_key=master_key)
            key = sk.key

        # Encode the key using base64. (b64decode() returns a bytestring under Python 3.)
        encoded_key = base64.b64encode(key).decode()

        # Craft the response
        response = Response({
            'session_key': encoded_key,
        })

        # If token authentication is not in use, assign the session key as a cookie
        if request.auth is None:
            response.set_cookie('session_key', value=encoded_key)

        return response