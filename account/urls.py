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
    path('admin/edit-billing/<pk>/', views.edit_billing_view, name="edit_billing"),
    path('admin/detail-billing/<pk>/', views.billing_detail_view, name="detail_billing"),
    path('admin/delete-billing/<pk>/', views.delete_billing_view, name="delete_billing"),

    path('admin/payment-list/', views.payment_list_view, name="payment_list"),
    path('admin/delete-payment/<pk>/', views.delete_payment_view, name="delete_payment"),

    path('admin/address-list/', views.add_and_view_addresses, name="address_list"),
    path('admin/make-default-address/<pk>/', views.make_default_address_view, name="make_default_address"),
    path('admin/delete-address/<pk>/', views.delete_address_view, name="delete_address"),
]
