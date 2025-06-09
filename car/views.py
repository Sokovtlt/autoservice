from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from custom.repeated_data import current_data, customer_data, reset_password_words
from custom.extra import CustomSuccessMessageMixin
from .models import Car, CarModel, CarBrand
from django.db.models import Q, Sum


class CarsView(LoginRequiredMixin, ListView, CustomSuccessMessageMixin):
    """To see orders for station"""
    model = Car
    context_object_name = 'get_car'
    template_name = 'cars_page.html'

    def get_context_data(self, **kwargs):
        # kwargs = output(self)
        current_user = self.request.user
        list_car = Car.objects.filter(author=current_user, deleted=False)
        kwargs['list_car'] = list_car
        if len(list_car) != 0:
            kwargs['car_block'] = True
        return super().get_context_data(**kwargs)
