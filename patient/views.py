from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .forms import PaymentForm
from account.models import Payment, Billing


def patient_dashboard_view(request):
    return render(request, 'account/patient/patient_dashboard.html')


def appointment_view(request):
    return render(request, 'account/patient/appointment.html')


def payment_view(request):
    payment_list = Payment.objects.filter(patient=request.user.patient)
    payment_count = payment_list.count()
    form = PaymentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            billing = Billing.objects.get(patient=request.user.patient)
            payment = form.save(commit=False)
            payment.patient = request.user.patient
            payment.billing = billing
            payment.save()
            messages.success(request, "Payment receipt uploaded successfully, awaiting verification. Thank you!")
            return redirect('patient:payment')
        
        except Billing.DoesNotExist:
            messages.error(request, "A bill has not been issued to this customer. please contact us for more information")

    context = {'payment_list':payment_list, 'form':form, 'payment_count':payment_count}
    return render(request, 'account/patient/payment.html', context)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        try:
            send_mail(
                'Message From '+name+' <'+email+'>',
                message,
                'contact@truecaremedservice.com',
                ['contact@truecaremedservice.com'],
                fail_silently=False,
            )
            messages.success(request, 'Email sent successfully, we will get back to you as soon as possible')
        except:
            messages.error(request, 'There was an error while trying to send your email, please try again')

        finally:
            return redirect('patient:contact')  
    return render(request, 'account/patient/contact.html')
