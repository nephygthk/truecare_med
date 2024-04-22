from django.urls import path

from . import views

app_name = 'frontend'
urlpatterns = [
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user_view, name='logout'),

    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),

    path('admin/add-patient/', views.add_patient_view, name="add_patient"),
    path('admin/edit-patient-info/<pk>/', views.edit_patient_view, name="edit_patient"),
    path('admin/delete-patient/<pk>/', views.delete_patient_account_view, name="delete_patient"),

    path('admin/doctors-list/', views.doctor_list_view, name="doctors_list"), 
    path('admin/delete-doctor/<pk>/', views.delete_doctor_view, name='delete_doctor'),   

    path('admin/bill-specification-list/', views.bill_specification_list_view, name="bill_spec_list"), 
    path('admin/delete-bill-specification/<pk>/', views.delete_billing_specification_view, name="delete_bill_spec"), 

    path('admin/billing-list/', views.billing_list_view, name="billing_list"),
    path('admin/add-new-billing/', views.add_new_billing_view, name="add_new_billing"),
]
