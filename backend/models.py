from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    fio = models.CharField(verbose_name='ФИО клиента', max_length=50)
    telephone = models.CharField(verbose_name='Контакный телефон', max_length=12)
    address = models.CharField(verbose_name='Адрес клиента', max_length=80, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        verbose_name_plural = 'customers'

    def __str__(self):
        return f'Клиент: {self.fio}, телефон: {self.telephone}'


class Device(models.Model):
    name = models.CharField(verbose_name='Устройство', max_length=50)
    model = models.CharField(verbose_name='Модель', max_length=50)
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=40)
    problem = models.CharField(verbose_name='Неисправность', max_length=120)

class Order(models.Model):
    STATUS = (
        ('open', 'Открыт'),
        ('work', 'Обслуживается'),
        ('done', 'Готов'),
        ('close', 'Закрыт'),
    )

    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS, max_length=5, default='open')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.PositiveIntegerField()
    summ = models.PositiveIntegerField(verbose_name='Сумма', default=0)
    text = models.TextField(verbose_name='Выполненная работа', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Заказ №{self.order_number}, принят {self.date_added}'


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text


class Cash(models.Model):
    name = models.CharField(verbose_name='Название кассы', max_length=30)
    money = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cashs')

    class Meta:
        verbose_name_plural = 'cash'

    def __str__(self):
        return f'{self.name}'
