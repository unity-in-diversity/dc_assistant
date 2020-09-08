from rest_framework import routers
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from Crypto.PublicKey import RSA
from rest_framework.response import Response

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