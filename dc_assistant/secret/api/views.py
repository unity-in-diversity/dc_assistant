from rest_framework import routers


class SecretsRootView(routers.APIRootView):
    """
    Secrets API root view
    """
    def get_view_name(self):
        return 'Secrets'