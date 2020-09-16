from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from secret.models import Secret


class SecretSerializer(ModelSerializer):
    plaintext = serializers.CharField()

    class Meta:
        model = Secret
        fields = [
            'id', 'name', 'plaintext', 'hash',
        ]
        validators = []

    def validate(self, data):

        # Encrypt plaintext using master key from view
        if data.get('plaintext'):
            s = Secret(plaintext=data['plaintext'])
            s.encrypt(self.context['master_key'])
            data['ciphertext'] = s.ciphertext
            data['hash'] = s.hash

        # Enforce model validation
        super().validate(data)

        return data
