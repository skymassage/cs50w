# Generated by Django 5.0.1 on 2024-03-02 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_price_listing_starting_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
    ]
