# Generated by Django 5.1.4 on 2024-12-13 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category_listings', to='auctions.category'),
        ),
    ]
