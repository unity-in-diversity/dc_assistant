from rest_framework.viewsets import ModelViewSet
from organisation.models import Device
from extend.filters import DeviceFilterSet
from .serializers import DeviceSerializer

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.prefetch_related(
        'device_model__vendor', 'device_role', 'platform', 'location', 'rack', 'tag',
    )
    filterset_class = DeviceFilterSet
    serializer_class = DeviceSerializer
