from rest_framework import routers
from .views import SecretsRootView



router = routers.DefaultRouter()
router.APIRootView = SecretsRootView

app_name = 'secrets-api'
urlpatterns = router.urls