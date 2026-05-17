from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваше ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше прізвище'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вулиця, будинок, квартира'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місто'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380XXXXXXXXX'}),
        }
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Email',
            'address': 'Адреса доставки',
            'city': 'Місто',
            'phone': 'Телефон',
        }


class CheckoutForm(forms.Form):
    """Alias for OrderCreateForm used in checkout"""
    pass
