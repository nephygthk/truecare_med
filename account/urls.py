from django.urls import path

from . import views

app_name = 'frontend'
urlpatterns = [
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user_view, name='logout'),

    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    
]
