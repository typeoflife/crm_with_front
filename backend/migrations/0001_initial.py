# Generated by Django 4.1.2 on 2022-11-29 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=50, verbose_name='ФИО клиента')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Контактный телефон')),
                ('address', models.CharField(blank=True, max_length=80, null=True, verbose_name='Адрес клиента')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Устройство')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('serial_number', models.CharField(max_length=40, verbose_name='Серийный номер')),
                ('problem', models.CharField(max_length=120, verbose_name='Неисправность')),
                ('kit', models.CharField(blank=True, default='Устройство', max_length=50, null=True, verbose_name='Комплект')),
                ('condition', models.CharField(blank=True, default='Б/У', max_length=70, null=True, verbose_name='Внешний вид')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('open', 'Открыт'), ('work', 'Обслуживается'), ('done', 'Готов'), ('close', 'Закрыт')], default='open', max_length=5, verbose_name='Статус заказа')),
                ('order_number', models.PositiveIntegerField()),
                ('summ', models.PositiveIntegerField(default=0, verbose_name='Сумма')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Выполненная работа')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customer')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='backend.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название кассы')),
                ('money', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cashs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'cash',
            },
        ),
    ]
