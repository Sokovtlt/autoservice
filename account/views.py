from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy, NoReverseMatch
from django.contrib import messages

from custom.repeated_data import current_data, customer_data, reset_password_words
from account.models import User
from .forms import *


#localization
W_MESSAGE_CREATE_USER = 'The user is created successfully'


class CustomSuccessMessageMixin:
    """The class for displaying a message when working with the form.
    The inherited classes receive the variable success_msg, and a message is passed in it"""
    @property
    def success_msg(self):
        return False

    def error_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg, self.error_msg)
        return super().form_valid(form)


class StartPageView(TemplateView):
    template_name = 'start_page.html'

    def get_context_data(self, **kwargs):
        kwargs = {**current_data(self), **customer_data(self)}
        print(kwargs['current_user'])
        return super().get_context_data(**kwargs)


class RegisterCustomerView(CreateView):
    model = User
    template_name = 'auth_reg/register_customer_page.html'
    form_class = RegisterCustomerForm
    success_url = reverse_lazy('dashboard_customer_page')
    success_msg = W_MESSAGE_CREATE_USER

    def get_context_data(self, **kwargs):
        kwargs = {**current_data(self), **customer_data(self)}
        current_user = kwargs['current_user']
        # current_customer = kwargs['current_customer']
        if kwargs['current_customer']:
            kwargs['logged'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # Проверяем, что форма валидна
        if not form.is_valid():
            print("Форма невалидна")
            print(form.errors)  # Логируем ошибки формы
            return self.form_invalid(form)
        self.object = form.save(commit=False)
        form_valid = super().form_valid(form)
        username = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
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
        # Сохранение пользователя
        try:
            self.object.save()  # Попробуем сохранить пользователя
        except Exception as e:
            # print(f"Ошибка при сохранении пользователя: {e}")
            form.add_error(None, "Error saving user")
            return self.form_invalid(form)
        aut_user = authenticate(username=username, password=password)
        # Проверка успешности аутентификации
        if aut_user is not None:
            login(self.request, aut_user)
        else:
            form.add_error(None, "Authentication failed. Please check your credentials.")
            return self.form_invalid(form)
        return form_valid


class RegisterStationView(CreateView):
    model = User
    template_name = 'auth_reg/register_station_page.html'
    form_class = RegisterStationForm
    success_url = reverse_lazy('dashboard_station_page')
    success_msg = W_MESSAGE_CREATE_USER

    def get_context_data(self, **kwargs):
        kwargs = current_data(self)
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


class UserLoginView(LoginView):
    template_name = 'auth_reg/login.html'
    form_class = AuthUserForm

    def get_context_data(self, **kwargs):
        kwargs = current_data(self)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="Stations").exists():
            return reverse('dashboard_station_page')
        elif user.groups.filter(name="Customers").exists():
            return reverse('dashboard_customer_page')
        else:
            return reverse_lazy('start_page')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('start_page')


class UserPasswordResetView(PasswordResetView):
    form_class = PassResetForm
    email_template_name = 'auth_reg/password_reset_email.html'
    template_name = 'auth_reg/password_reset_form.html'

    def get_context_data(self, **kwargs):
        kwargs = reset_password_words(self)
        return super().get_context_data(**kwargs)


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'auth_reg/password_reset_done.html'
    title = ('Password reset sent')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth_reg/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        kwargs = reset_password_words(self)
        return super().get_context_data(**kwargs)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth_reg/password_reset_complete.html'
    title = ('Password reset complete')

    def get_context_data(self, **kwargs):
        kwargs = reset_password_words(self)
        return super().get_context_data(**kwargs)


class DashboardCustomerView(LoginRequiredMixin, ListView):
    """To see cars and orders for customer"""
    model = Customer
    context_object_name = 'get_customer'
    template_name = 'customer/dashboard_cs.html'

    def get_context_data(self, **kwargs):
        kwargs = {**current_data(self), **customer_data(self)}

        return super().get_context_data(**kwargs)


class DetailCustomerView(LoginRequiredMixin, DetailView, CustomSuccessMessageMixin):
    """Info about a customer"""
    model = Customer
    template_name = 'customer/customer.html'
    context_object_name = 'get_customer'

    def get_context_data(self, **kwargs):
        kwargs = {**current_data(self), **customer_data(self)}
        current_user = self.object
        # kwargs['list_car'] = Car.objects.filter(Q(author=current_user) & Q(deleted=False))
        kwargs['customer_url'] = True
        return super().get_context_data(**kwargs)
