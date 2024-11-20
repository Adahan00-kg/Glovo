# Generated by Django 5.1.3 on 2024-11-19 05:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0007_cart_courier_cart_courier_combo_comboproduct_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comboproduct',
            old_name='quantity',
            new_name='quantity_combo',
        ),
        migrations.RemoveField(
            model_name='store',
            name='owner',
        ),
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]