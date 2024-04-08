from django.shortcuts import render

def home(request):
    return render(request, 'frontend/home.html')


def about(request):
    return render(request, 'frontend/about.html')


def service(request):
    return render(request, 'frontend/service.html')


def contact(request):
    return render(request, 'frontend/contact.html')
