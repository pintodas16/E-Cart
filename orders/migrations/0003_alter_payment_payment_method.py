# Generated by Django 4.0.4 on 2022-05-28 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20220527_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=200),
        ),
    ]
