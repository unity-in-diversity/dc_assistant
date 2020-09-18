from django.shortcuts import render
from collections import OrderedDict
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from organisation.models import Region, Location, Rack, VendorModel, Device
from secret.models import Secret
# Create your views here.

class MainView(View):
    template_name = 'home.html'

    def get(self, request):

        stats = {

            # Organization
            'region_count': Region.objects.count(),
            'location_count': Location.objects.count(),
            'rack_count': Rack.objects.count(),
            'devicemodel_count': VendorModel.objects.count(),
            'device_count': Device.objects.count(),

            # Secrets
            'secret_count': Secret.objects.count(),

        }

        return render(request, self.template_name, {
            'stats': stats,
        })


    # def get(self, request):
    #
    #     return render(request, self.template_name)


class APIRootView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    swagger_schema = None

    def get_view_name(self):
        return "API Root"

    def get(self, request, format=None):

        return Response(OrderedDict((
            ('secrets', reverse('secrets-api:api-root', request=request, format=format)),
            ('organisation', reverse('organisation-api:api-root', request=request, format=format)),
        )))
