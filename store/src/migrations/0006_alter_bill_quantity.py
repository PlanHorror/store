# Generated by Django 5.1.3 on 2024-11-14 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0005_alter_bill_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
