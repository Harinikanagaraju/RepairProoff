
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='tracker/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('appliances/', views.appliance_list, name='appliances'),

    path(
        'appliances/add/',
        views.add_appliance,
        name='add_appliance'
    ),

    path(
        'appliances/edit/<int:pk>/',
        views.edit_appliance,
        name='edit_appliance'
    ),

    path(
        'appliances/delete/<int:pk>/',
        views.delete_appliance,
        name='delete_appliance'
    ),

    path('repairs/', views.repair_list, name='repairs'),

    path(
        'repairs/add/',
        views.add_repair,
        name='add_repair'
    ),
]