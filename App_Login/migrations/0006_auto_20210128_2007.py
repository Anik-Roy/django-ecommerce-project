# Generated by Django 3.1.5 on 2021-01-28 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Login', '0005_sellerinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerinfo',
            name='shop_address',
            field=models.TextField(blank=True, max_length=350),
        ),
        migrations.AlterField(
            model_name='sellerinfo',
            name='shop_name',
            field=models.CharField(blank=True, max_length=264),
        ),
        migrations.AlterField(
            model_name='sellerinfo',
            name='shop_type',
            field=models.CharField(blank=True, choices=[('electronics', 'Electronics'), ('accessories', 'Accessories'), ('cloths', 'Cloths'), ('groceries', 'Groceries'), ('others', 'Others')], max_length=50),
        ),
    ]
