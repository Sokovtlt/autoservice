from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea
from .models import *
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User


from django.contrib.auth import get_user_model
User = get_user_model()


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'your username'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PassResetForm(PasswordResetForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'your email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'titul',
            'first_name',
            'last_name',
            'phone',
            'email',
            'city',
            'street',
            'address_code',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'required'
        self.fields['phone'].widget.attrs['placeholder'] = 'optional'
        self.fields['address_code'].widget.attrs['placeholder'] = 'optional'
        self.fields['first_name'].widget.attrs['placeholder'] = 'required'
        self.fields['last_name'].widget.attrs['placeholder'] = 'required'
        self.fields['city'].widget.attrs['placeholder'] = 'required'
        self.fields['street'].widget.attrs['placeholder'] = 'optional'
        self.fields['titul'].widget.attrs['placeholder'] = 'optional'
        self.fields['first_name'].widget.attrs['required'] = 'True'
        self.fields['last_name'].widget.attrs['required'] = 'True'
        # self.fields['phone'].widget.attrs['required'] = 'True'
        self.fields['email'].widget.attrs['required'] = 'True'
        self.fields['city'].widget.attrs['required'] = 'True'
        self.fields['password'].widget.attrs['required'] = 'True'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        username = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Username {username} is already taken")
        if commit:
            user.save()
        return user


class RegisterStationForm(forms.ModelForm):
    district_choice = [
        ('1', 'Wien'),
        ('2', 'Niederösterreich'),
        ('3', 'Burgenland'),
        ('4', 'Steiermark'),
        ('5', 'Oberösterreich'),
        ('6', 'Salzburg'),
        ('7', 'Kärnten'),
        ('8', 'Nordtirol'),
        ('9', 'Osttirol'),
        ('10', 'Vorarlberg'),
    ]
    district = forms.ChoiceField(choices=district_choice, widget=forms.RadioSelect)
    class Meta:
        model = Station
        fields = (
            'titul',
            'first_name',
            'last_name',
            'email',
            'phone',
            'name_stat',
            'name_comp',
            'district',
            'city',
            'street',
            'house',
            'address_code',
            'web_site',
            'file_atu',
            'uid',
            'cash',
            'card',
            'transfer',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['placeholder'] = '+430000000000'
        self.fields['titul'].widget.attrs['placeholder'] = 'optional'
        self.fields['first_name'].widget.attrs['required'] = 'True'
        self.fields['first_name'].widget.attrs['placeholder'] = 'required'
        self.fields['last_name'].widget.attrs['required'] = 'True'
        self.fields['last_name'].widget.attrs['placeholder'] = 'required'
        self.fields['phone'].widget.attrs['required'] = 'True'
        self.fields['phone'].widget.attrs['placeholder'] = 'required'
        self.fields['email'].widget.attrs['required'] = 'True'
        self.fields['email'].widget.attrs['placeholder'] = 'required'
        self.fields['city'].widget.attrs['required'] = 'True'
        self.fields['city'].widget.attrs['placeholder'] = 'required'
        self.fields['street'].widget.attrs['required'] = 'True'
        self.fields['street'].widget.attrs['placeholder'] = 'required'
        self.fields['house'].widget.attrs['required'] = 'True'
        self.fields['house'].widget.attrs['placeholder'] = 'required'
        self.fields['address_code'].widget.attrs['required'] = 'True'
        self.fields['address_code'].widget.attrs['placeholder'] = 'required'
        self.fields['password'].widget.attrs['required'] = 'True'
        self.fields['name_stat'].widget.attrs['required'] = 'True'
        self.fields['name_stat'].widget.attrs['placeholder'] = 'required'
        self.fields['name_comp'].widget.attrs['required'] = 'True'
        self.fields['name_comp'].widget.attrs['placeholder'] = 'required'
        self.fields['uid'].widget.attrs['required'] = 'True'
        self.fields['uid'].widget.attrs['placeholder'] = 'required'
        self.fields['file_atu'].widget.attrs['required'] = 'True'
        self.fields['file_atu'].widget.attrs['placeholder'] = 'required'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['card'].widget.attrs['class'] = 'my-checkbox'
        self.fields['cash'].widget.attrs['class'] = 'my-checkbox'
        self.fields['transfer'].widget.attrs['class'] = 'my-checkbox'
        self.fields['district'].widget.attrs['class'] = 'map-block-input'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
