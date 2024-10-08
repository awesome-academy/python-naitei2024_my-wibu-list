# Generated by Django 4.2.15 on 2024-08-16 04:40

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wibu_catalog', '0006_merge_0002_auto_20240815_1228_0005_auto_20240813_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, help_text='Content cover picture.', max_length=255, null=True),
        ),
    ]
