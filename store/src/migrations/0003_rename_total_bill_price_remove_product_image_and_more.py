# Generated by Django 5.1.3 on 2024-11-14 08:42

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_product_bill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='total',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='bill',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='src.product'),
        ),
        migrations.AddField(
            model_name='bill',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
    ]