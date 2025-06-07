from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.StartPageView.as_view(), name='start_page'),
    # auth and reg
    path('register-customer/', views.RegisterCustomerView.as_view(), name='register_customer_page'),
    path('register-station/', views.RegisterStationView.as_view(), name='register_station_page'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login_page'),
    path('accounts/logout/', views.UserLogoutView.as_view(), name='logout_page'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetDone.as_view(), name='password_reset_done'),
    re_path(
        r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('password-reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # # customer
    path('customer/<slug:slug>/', views.DetailCustomerView.as_view(), name='detail_customer_page'),
    path('your-dashboard/', views.DashboardCustomerView.as_view(), name='dashboard_customer_page'),
]
