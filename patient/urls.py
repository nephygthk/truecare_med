from django.urls import path

from . import views

app_name = 'patient'
urlpatterns = [
    path('patiend/dashboard', views.patient_dashboard_view, name='patient_dashboard'),
]