from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy, NoReverseMatch

from custom.repeated_data import output
from account.models import User
from .forms import *


#localization
W_MESSAGE_CREATE_USER = 'The user is created successfully'


class StartPageView(TemplateView):
    template_name = 'start_page.html'

    def get_context_data(self, **kwargs):
        kwargs = output(self)
        return super().get_context_data(**kwargs)


class RegisterCustomerView(CreateView):
    model = User
    template_name = 'auth_reg/register_customer_page.html'
    form_class = RegisterCustomerForm
    success_url = reverse_lazy('cars_page')
    success_msg = W_MESSAGE_CREATE_USER

    def get_context_data(self, **kwargs):
        kwargs = output(self)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form_valid = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        try:
            customers_group = Group.objects.get(name='Customers')
        except ObjectDoesNotExist:
            Group.objects.create(name='Customers')
            customers_group = Group.objects.get(name='Customers')
        self.object.groups.add(customers_group)
        self.object.is_active = True
        if self.object.email:
            self.object.slug = str(self.object.email).replace('.', '-').replace('@', '-a-')
            self.object.username = self.object.email
        self.object.save()
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class RegisterStationView(CreateView):
    model = User
    template_name = 'auth_reg/register_station_page.html'
    form_class = RegisterStationForm
    success_url = reverse_lazy('dashboard_station_page')
    success_msg = W_MESSAGE_CREATE_USER

    def get_context_data(self, **kwargs):
        kwargs = output(self)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form_valid = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        try:
            stations_group = Group.objects.get(name='Stations')
        except ObjectDoesNotExist:
            Group.objects.create(name='Stations')
            stations_group = Group.objects.get(name='Stations')
        self.object.groups.add(stations_group)
        self.object.is_active = True
        if self.object.email:
            self.object.slug = str(self.object.email).replace('.', '-').replace('@', '-a-')
            self.object.username = self.object.email
        self.object.save()
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid
