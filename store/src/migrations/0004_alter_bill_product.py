# Generated by Django 5.1.3 on 2024-11-14 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0003_rename_total_bill_price_remove_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.product'),
        ),
    ]