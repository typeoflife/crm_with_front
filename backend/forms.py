from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from backend.models import Order, Device, Customer, Cash


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('fio', 'phone', 'address',)

        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
        }


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ('name', 'model', 'serial_number', 'problem', 'kit', 'condition')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'problem': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'kit': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
            'condition': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
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

class CashForm(ModelForm):
    class Meta:
        model = Cash
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:45%'}),
        }

    # all_user_cash = Cash.objects.filter(user_id=request.user).values_list('name', flat=True)
    # print(all_user_cash)
    # if cash.name in all_user_cash:

# class ChoiseCash(ModelForm):
#     class Meta:
#         model = Order
#         fields = ('status',)
#         STATUS_CHOICES = (
#             ('open', 'Открыт'),
#             ('work', 'Обслуживается'),
#             ('done', 'Готов'),
#             ('close', 'Закрыт'),
#         )
#         widgets = {
#             'status': forms.Select(choices=STATUS_CHOICES,
#                                    attrs={'class': 'form-control form-control-sm', 'style': 'width:auto'}),
#         }