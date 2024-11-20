# Generated by Django 5.1.3 on 2024-11-19 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0013_cart_combo_alter_cart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status_book',
        ),
        migrations.AddField(
            model_name='courier',
            name='status_book',
            field=models.CharField(choices=[('ожидания', 'ожидания'), ('в пути', 'в пути'), ('доставлено', 'доставлено')], default=1, max_length=25),
            preserve_default=False,
        ),
    ]
