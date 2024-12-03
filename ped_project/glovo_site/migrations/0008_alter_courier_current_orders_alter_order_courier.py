# Generated by Django 5.1.3 on 2024-11-22 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0007_order_courier_alter_order_status_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='current_orders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_orders', to='glovo_site.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courier_order', to=settings.AUTH_USER_MODEL),
        ),
    ]