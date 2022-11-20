from django import forms
from django.forms import ModelForm

from backend.models import Order, Device, Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('fio', 'telephone', 'address',)

        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
        }


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ('name', 'model', 'serial_number',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
        }


class EditOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status', 'summ', 'text',)
        STATUS_CHOICES = (
            ('open', 'Открыт'),
            ('work', 'Обслуживается'),
            ('done', 'Готов'),
            ('close', 'Закрыт'),
        )
        widgets = {
            'status': forms.Select(choices=STATUS_CHOICES,
                                   attrs={'class': 'form-control form-control-sm', 'style': 'width:auto'}),
            'summ': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:auto'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:65%'}),
        }
