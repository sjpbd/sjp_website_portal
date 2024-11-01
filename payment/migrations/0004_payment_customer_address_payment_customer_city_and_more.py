# Generated by Django 5.1.2 on 2024-10-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_payment_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='customer_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_postcode',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('BDT', 'Bangladeshi Taka'), ('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound')], default='BDT', max_length=3),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('VISA', 'Visa Card'), ('MASTER', 'Master Card'), ('AMEX', 'American Express'), ('BKASH-BKash', 'bKash'), ('NAGAD-Nagad', 'Nagad'), ('ROCKET-Rocket', 'Rocket')], max_length=50),
        ),
    ]