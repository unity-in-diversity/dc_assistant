from rest_framework import routers
from .views import SecretsRootView, GenerateRSAKeyPairViewSet, GetSessionKeyViewSet



router = routers.DefaultRouter()
router.APIRootView = SecretsRootView

router.register('get-session-key', GetSessionKeyViewSet, basename='get-session-key')
router.register('generate-rsa-key-pair', GenerateRSAKeyPairViewSet, basename='generate-rsa-key-pair')

app_name = 'secrets-api'
urlpatterns = router.urls