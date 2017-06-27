from django.shortcuts import render

# Create your views here.


def home_page(request):
    # builds an HttpResponse
    return render(request, 'home.html')
