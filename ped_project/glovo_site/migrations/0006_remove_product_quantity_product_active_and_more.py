# Generated by Django 5.1.3 on 2024-11-18 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glovo_site', '0005_alter_userprofile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='в наличии'),
        ),
        migrations.AddField(
            model_name='review',
            name='parent_review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='glovo_site.review'),
        ),
        migrations.AlterField(
            model_name='review',
            name='product_ratting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='glovo_site.product'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=16)),
                ('store_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_category', to='glovo_site.store')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product', to='glovo_site.category'),
        ),
    ]