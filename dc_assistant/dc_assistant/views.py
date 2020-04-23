from django.shortcuts import render

# Create your views here.

def main_view(request):
    pass
    return render(request, 'home.html', context={})
