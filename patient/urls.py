from django.urls import path

from . import views

app_name = 'patient'
urlpatterns = [
    path('patiend/dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    path('patiend/appointments/', views.appointment_view, name='appointment_list'),
    path('patiend/payment/', views.payment_view, name='payment'),
    path('patiend/contact/', views.contact_view, name='contact'),
]