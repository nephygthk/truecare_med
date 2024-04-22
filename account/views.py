from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Patient, Doctor, BillingSpecification
from .forms import (PatientForm, RegistrationForm, CustomerUpdateForm,
                    AddDoctorForm, BillSpecificationForm)


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
    patient_list = Customer.objects.filter(is_staff=False)
    patients_count = patient_list.count()

    context = {'patient_list':patient_list, 'patient_count':patients_count}
    return render(request, 'account/admin/admin_dashboard.html', context)


@login_required
def add_patient_view(request):
    customer_form = RegistrationForm(request.POST or None)
    patient_form = PatientForm(request.POST or None, request.FILES or None)

    if customer_form.is_valid() and patient_form.is_valid():
        user = customer_form.save(commit=False)
        user.set_password(customer_form.cleaned_data["password"])
        user.save()
        patient = patient_form.save(commit=False)
        patient.customer = user
        patient.pass_text = customer_form.cleaned_data["password"]
        patient.save()
        messages.success(request, 'Patient was added successfully')
        return redirect('account:add_patient')

    context = {'form': customer_form, 'patient_form':patient_form}
    return render(request, 'account/admin/add_patient.html', context)


@login_required
def edit_patient_view(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    patient = Patient.objects.get(customer=customer)
    customer_form = CustomerUpdateForm(request.POST or None, instance=customer)
    patient_form = PatientForm(request.POST or None, request.FILES or None, instance=patient)

    if customer_form.is_valid() and patient_form.is_valid():
        customer_form.save()
        patient = patient_form.save()
        messages.success(request, 'Patient was updated successfully')
        return redirect('account:admin_dashboard')

    context = {'form': customer_form, 'patient_form':patient_form}
    return render(request, 'account/admin/edit_patient.html', context)


@login_required
def delete_patient_account_view(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    customer.delete()
    messages.success(request, 'Patient deleted successfully')
    return redirect('account:admin_dashboard')


@login_required
def doctor_list_view(request):
    doctors = Doctor.objects.all()
    doctor_count = doctors.count()
    form = AddDoctorForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Doctor was added successfully')
        return redirect('account:doctors_list')
    
    context = {'doctor_list':doctors, 'doctor_count':doctor_count, 'form':form}
    return render(request, 'account/admin/list_doctors.html', context)


@login_required
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    doctor.delete()
    messages.success(request, 'Doctor deleted successfully')
    return redirect('account:doctors_list')


@login_required
def bill_specification_list_view(request):
    spec_list = BillingSpecification.objects.all()
    spec_count = spec_list.count()
    form = BillSpecificationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Doctor was added successfully')
        return redirect('account:doctors_list')
    
    context = {'spec_list':spec_list, 'spec_count':spec_count, 'form':form}
    return render(request, 'account/admin/list_bill_spec.html', context)
