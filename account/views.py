from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import (Customer, Patient, Doctor, BillingSpecification, 
                    Billing, BillingItem, Payment, Address)
from .forms import (PatientForm, RegistrationForm, CustomerUpdateForm,
                    AddDoctorForm, BillSpecificationForm, BillingForm, BillingItemFormSet, EditBillingItemFormSet, AddressForm)


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
        messages.success(request, 'Bill specification was added successfully')
        return redirect('account:bill_spec_list')
    
    context = {'spec_list':spec_list, 'spec_count':spec_count, 'form':form}
    return render(request, 'account/admin/list_bill_spec.html', context)


@login_required
def delete_billing_specification_view(request, pk):
    billing_spec = get_object_or_404(BillingSpecification, id=pk)
    billing_spec.delete()
    messages.success(request, 'Bill Specification deleted successfully')
    return redirect('account:bill_spec_list')


@login_required
def billing_list_view(request):
    billing_list = Billing.objects.all()
    billing_count = billing_list.count()

    context = {'billing_list':billing_list, 'billing_count':billing_count}
    return render(request, 'account/admin/list_billing.html', context)


@login_required   
def add_new_billing_view(request):
    if request.method == "POST":
        form = BillingForm(request.POST)
        formset = BillingItemFormSet(request.POST)
        try:
            if form.is_valid and formset.is_valid():
                prices = []
                parent = form.save()
                for form in formset:
                    child = form.save(commit=False)
                    child.billing = parent
                    child.save()
                    prices.append(int(child.bill_value) * (int(child.bill_qty)))

                parent.bill_amount = sum(Decimal(price)  for price in prices)
                parent.save()
                return redirect('account:billing_list')
        except ValueError:
            messages.success(request, 'A bill for this patient already exist')
            return redirect('account:add_new_billing')
    else:
        form = BillingForm()
        formset = BillingItemFormSet()
    context = {'billing_form':form, 'bill_item_form':formset }
    return render(request, 'account/admin/add_billing.html', context )


@login_required
def edit_billing_view(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    billing_item = BillingItem.objects.filter(billing=billing)
    form = BillingForm(request.POST or None, instance=billing)
    formset = EditBillingItemFormSet(request.POST or None, queryset=billing_item)

    if all([form.is_valid(), formset.is_valid()]):
        prices = []
        parent = form.save()
        for form in formset:
            child = form.save(commit=False)
            child.billing = parent
            child.save()
            prices.append(int(child.bill_value) * (int(child.bill_qty)))
        parent.bill_amount = sum(Decimal(price)  for price in prices)
        parent.save()

        messages.success(request, 'The bill was updated successfully')
        return redirect('account:billing_list')

    context = {'billing_form':form, 'bill_item_form':formset}
    return render(request, "account/admin/edit_billing.html", context)


@login_required
def billing_detail_view(request, pk):
    billing_detail =  get_object_or_404(Billing, pk=pk)
    bill_items = BillingItem.objects.filter(billing=billing_detail)

    context = {'bill':billing_detail, 'bill_items':bill_items}
    return render(request, "account/admin/list_billing_detail.html", context)


@login_required
def delete_billing_view(request, pk):
    billing = get_object_or_404(Billing, id=pk)
    billing.delete()
    messages.success(request, 'Billing deleted successfully')
    return redirect('account:billing_list')


@login_required
def payment_list_view(request):
    payment_list = Payment.objects.all()
    payment_count = payment_list.count()

    context = {'payment_list':payment_list, 'payment_count':payment_count}
    return render(request, 'account/admin/list_payment.html', context)


@login_required
def delete_payment_view(request, pk):
    payment = get_object_or_404(Payment, id=pk)
    payment.delete()
    messages.success(request, 'payment deleted successfully')
    return redirect('account:payment_list')


@login_required
def add_and_view_addresses(request):
    list_address = Address.objects.all()
    address_count = list_address.count()
    address_form = AddressForm(request.POST or None)

    if address_form.is_valid():
        address_form.save()
        messages.info(request, 'The new address was added successfully')
        return redirect('account:address_list')

    context = {'form':address_form, 'list_address':list_address,'address_count':address_count }
    return render(request, 'account/admin/list_address.html', context)


@login_required
def make_default_address_view(request, pk):
    Address.objects.filter(is_default=True).update(is_default=False)
    Address.objects.filter(pk=pk).update(is_default=True)
    return redirect('account:address_list')


@login_required
def delete_address_view(request, pk):
    address = Address.objects.get(id=pk)
    if address.is_default == True:
        messages.error(request, "This address can't be delected because it is currently selected as the default address. remove it as default address before deleting")
    else:
        address.delete()
        messages.success(request, 'Address deleted successfully')
    return redirect('account:address_list')

