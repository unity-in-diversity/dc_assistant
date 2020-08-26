from django.shortcuts import render
from django.views.generic import View
# Create your views here.

class MainView(View):
    template_name = 'home.html'

    def get(self, request):

        return render(request, self.template_name)
