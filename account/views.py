from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_user_view(request):

    # check if user is already authenticated
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('account:admin_dashboard')
        # else:
        #     return redirect('account:patient_status')
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('account:admin_dashboard')
            # else:
            #     login(request, user)
            #     return redirect('account:patient_dashboard')
            
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('frontend:home')

        return redirect('/')
    return render(request, 'frontend/home.html')


@login_required
def logout_user_view(request):
    logout(request)
    return redirect('/')


@login_required
def admin_dashboard(request):
    return render(request, 'account/admin/admin_dashboard.html')
