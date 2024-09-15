from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator

import datetime

from .managers import UserManager
from custom.extra import validate_file_size


# for localization
W_FIRST_NAME = 'first name'
W_LAST_NAME = 'last name'
W_EMAIL_ADDRESS = 'email address'
W_PHONE_NUMBER = 'phone number'
W_TITUL = 'titul'
W_CITY = 'City'
W_STREET = 'Street and number of your building'
W_ADDRESS_CODE = 'Address code'

W_NAME_OF_STATION = 'Name of the station'
W_NAME_OF_COMPANY = 'Name of the company'
W_NUMBER_OF_BUILDING = 'Number of the building'


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.username, filename)


def station_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, unique=True)
    first_name = models.CharField(_(W_FIRST_NAME), max_length=255)
    last_name = models.CharField(_(W_LAST_NAME), max_length=255)
    email = models.EmailField(_(W_EMAIL_ADDRESS), null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?(\d){6,18}$',
        message="Phone number must be entered in the format: '+431234567890' or 01234567890"
    )
    phone = models.CharField(_(W_PHONE_NUMBER), null=True, blank=True, validators=[phone_regex], max_length=17)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='default_user',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='default_permission',
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = ('email', 'phone')


class Customer(User, models.Model):
    """The customer"""
    titul_choice = [
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),
        ('Fräulein', 'Fräulein'),
        ('Professor', 'Professor'),
        ('PD', 'PD'),
        ('Doktor', 'Doktor'),
        ('Magister', 'Magister'),
        ('Ingenieur', 'Ingenieur'),
    ]
    user_rate = models.FloatField('Rate', null=True, blank=True)
    total_rate = models.IntegerField('SUM rate', null=True, blank=True)
    rate_number = models.IntegerField('Rate number', null=True, blank=True)
    titul = models.CharField(W_TITUL, max_length=50, null=True, blank=True, choices=titul_choice)
    city = models.CharField(W_CITY, max_length=100)
    street = models.CharField(W_STREET, max_length=100, null=True, blank=True)
    address_code = models.IntegerField(W_ADDRESS_CODE, null=True, blank=True)
    slug = models.SlugField('slug', unique=True)
    create_date = models.DateTimeField('Date of registration', auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Station(User, models.Model):
    """The service station"""
    titul_choice = [
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),
        ('Fräulein', 'Fräulein'),
        ('Professor', 'Professor'),
        ('PD', 'PD'),
        ('Doktor', 'Doktor'),
        ('Magister', 'Magister'),
        ('Ingenieur', 'Ingenieur'),
    ]
    titul = models.CharField(W_TITUL, max_length=50, null=True, blank=True, choices=titul_choice)
    station_rate = models.FloatField('Rate', null=True, blank=True)
    name_stat = models.CharField(W_NAME_OF_STATION, max_length=100)
    name_comp = models.CharField(W_NAME_OF_COMPANY, max_length=100)
    city = models.CharField(W_CITY, max_length=100)
    street = models.CharField(W_STREET, max_length=100)
    house = models.CharField('Number of the building', max_length=100)
    address_code = models.IntegerField(W_ADDRESS_CODE)
    web_site = models.CharField('Web site', max_length=100, null=True, blank=True)
    file_atu = models.FileField('Upload your ATU', upload_to=station_directory_path, null=True, blank=True,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png']),
                                            validate_file_size]
                                )
    uid = models.CharField('UID', max_length=50)
    cash = models.BooleanField('Cash', default=False)
    card = models.BooleanField('Card', default=False)
    transfer = models.BooleanField('Bank transfer', default=False)
    slug = models.SlugField('slug', unique=True)
    create_date = models.DateTimeField('Date of registration', auto_now_add=True)
    district_choice = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]
    district = models.CharField(
        max_length=30,
        verbose_name='District',
        choices=district_choice,
    )
    middle_rate = models.FloatField('Middle rate', null=True, blank=True)
    total_rate = models.IntegerField('SUM rate', null=True, blank=True)
    offer_number = models.IntegerField('Confirm offer number', default=0)

    def __str__(self):
        return '%s - %s' % (self.name_stat, self.city)

    class Meta:
        verbose_name = 'Service station'
        verbose_name_plural = 'Service stations'
