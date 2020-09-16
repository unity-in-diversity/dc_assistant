from rest_framework import routers

from . import views


class OrganisationRootView(routers.APIRootView):
    """
    Organisation API root view
    """
    def get_view_name(self):
        return 'Organisation'

router = routers.DefaultRouter()
router.APIRootView = OrganisationRootView

router.register('devices', views.DeviceViewSet)

app_name = 'organisation-api'
urlpatterns = router.urls