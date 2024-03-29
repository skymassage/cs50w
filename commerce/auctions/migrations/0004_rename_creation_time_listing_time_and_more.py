# Generated by Django 5.0.1 on 2024-02-29 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_comment_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='creation_time',
            new_name='time',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
