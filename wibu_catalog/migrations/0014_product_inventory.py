# Generated by Django 4.2.15 on 2024-08-29 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wibu_catalog', '0013_merge_20240827_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='inventory',
            field=models.IntegerField(default=0),
        ),
    ]
