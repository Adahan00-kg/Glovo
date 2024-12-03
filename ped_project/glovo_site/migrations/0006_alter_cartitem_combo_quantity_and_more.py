# Generated by Django 5.1.3 on 2024-11-22 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0005_alter_cartitem_combo_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='combo_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество комбо продуктов'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product_quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество продуктов'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glovo_site.cartitem'),
        ),
    ]