from django.db import models
import datetime
from django.core.validators import FileExtensionValidator

from account.models import Customer, user_directory_path
from custom.extra import validate_file_size


W_BRAND = 'Brand of car'
W_MODEL = 'Car model'


class CarBrand(models.Model):
    """The list of models"""
    brand = models.CharField(W_BRAND, max_length=200)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Car Brand'
        verbose_name_plural = 'Car Brands'


class CarModel(models.Model):
    """The list of models"""
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, verbose_name='Car brand')
    model = models.CharField(W_MODEL, max_length=200)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'


class Car(models.Model):
    """The user car, which add the customer in his account"""
    years_list = []
    for i in range(1950, datetime.date.today().year + 1):
        t = (i, i)
        years_list.append(t)
    years_list.reverse()
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Car author', null=True)
    name = models.CharField('Name car', max_length=200, null=True, blank=True)
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE,
                                  verbose_name='Car brand', null=True, blank=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Car model', null=True, blank=True)
    vin = models.CharField('Vin code', max_length=30, null=True, blank=True)
    file_pass_1 = models.FileField('Upload photo front side of your car pas', upload_to=user_directory_path, null=True,
                                   blank=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png']),
                                               validate_file_size])
    file_pass_2 = models.FileField('Upload photo back side of your car pas', upload_to=user_directory_path, null=True,
                                   blank=True,
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png']),
                                               validate_file_size])
    old = models.IntegerField('Car year', choices=years_list, null=True, blank=True)
    color = models.CharField('Car color', max_length=50)
    slug = models.SlugField('slug', unique=True)
    run = models.IntegerField('Car mileage')
    create_date = models.DateTimeField('Date of adding', auto_now_add=True)
    text = models.TextField('Description')
    deleted = models.BooleanField('This car is deleted', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
