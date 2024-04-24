from django.shortcuts import render

def patient_dashboard_view(request):
    return render(request, 'account/patient/patient_dashboard.html')
