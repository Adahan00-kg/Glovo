# Generated by Django 5.1.3 on 2024-11-18 09:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxLengthValidator(100)]),
        ),
    ]
