from django.shortcuts import render, redirect

from account.models import Address

def home(request):
    
    # check if user is already authenticated
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('account:admin_dashboard')
        # else:
        #     return redirect('account:patient_status')

    address = Address.objects.get(is_default=True)
    context ={'address':address}
    return render(request, 'frontend/home.html', context)


def about(request):
    address = Address.objects.get(is_default=True)
    context ={'address':address}
    return render(request, 'frontend/about.html', context)


def service(request):
    address = Address.objects.get(is_default=True)
    context ={'address':address}
    return render(request, 'frontend/service.html', context)


def contact(request):
    address = Address.objects.get(is_default=True)
    
    context ={'address':address}
    return render(request, 'frontend/contact.html', context)
