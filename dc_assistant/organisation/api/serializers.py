from rest_framework.serializers import ModelSerializer
from organisation.models import Device

class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        fields = [
            'id', 'name', 'display_name', 'device_model', 'device_role', 'platform', 'serial',
            'location', 'rack', 'position', 'face_position', 'created', 'last_updated',
        ]
