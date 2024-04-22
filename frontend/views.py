from django.shortcuts import render, redirect

def home(request):
    
    # check if user is already authenticated
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('account:admin_dashboard')
        # else:
        #     return redirect('account:patient_status')

    return render(request, 'frontend/home.html')


def about(request):
    return render(request, 'frontend/about.html')


def service(request):
    return render(request, 'frontend/service.html')


def contact(request):
    return render(request, 'frontend/contact.html')
