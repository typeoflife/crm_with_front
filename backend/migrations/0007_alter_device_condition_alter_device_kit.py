# Generated by Django 4.1.2 on 2022-11-28 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_device_condition_alter_device_kit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='condition',
            field=models.CharField(blank=True, default='Б/У', max_length=70, null=True, verbose_name='Внешний вид'),
        ),
        migrations.AlterField(
            model_name='device',
            name='kit',
            field=models.CharField(blank=True, default='Устройство', max_length=50, null=True, verbose_name='Комплект'),
        ),
    ]