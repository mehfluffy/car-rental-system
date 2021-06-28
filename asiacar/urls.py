from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rent/', views.rent_view, name='rent'),
    path('rent/checkout/', views.checkout_view, name='rentcheckout'),
    path('rent/checkout/success/', views.checkout_success_view, name='rentsuccess'),
    path('return/', views.return_view, name='return'),
    path('return/success/', views.return_success_view, name='returnsuccess'),
]