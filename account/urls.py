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
    # path('customer/edit/<slug:slug>/', views.UpdateCustomerView.as_view(), name='update_customer_page'),
    path('your-dashboard/', views.DashboardCustomerView.as_view(), name='dashboard_customer_page'),
    # # station
    # path('station/<slug:slug>/', views.DetailStationView.as_view(), name='detail_station_page'),
    # path('station/edit/<slug:slug>/', views.UpdateStationView.as_view(), name='update_station_page'),
    # path('dashboard/', views.DashboardStationView.as_view(), name='dashboard_station_page'),
    # # support customer
    # path('customer-support/', views.SupportCsView.as_view(), name='customer_sp_page'),
    # path('customer-ticket/<int:pk>/', views.DetailSupportCsView.as_view(), name='detail_support_cs_page'),
    # # support station
    # path('station-support/', views.SupportStView.as_view(), name='station_sp_page'),
    # path('station-ticket/<int:pk>/', views.DetailSupportStView.as_view(), name='detail_support_st_page'),
    # # admin
    # path('admin-checking-offers-for-date/', views.CheckingOffersView.as_view(), name='admin_checking_offers_page'),
    # path('test/', views.TestView.as_view(), name='test'),
    # path('owner-dashboard/', views.OwnerDashboardView.as_view(), name='dashboard_owner_page'),
    # path('support-dashboard/', views.SupportDashboardView.as_view(), name='dashboard_support_page'),
]
