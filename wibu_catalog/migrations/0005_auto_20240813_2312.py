# Generated by Django 3.2.25 on 2024-08-13 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wibu_catalog', '0004_rename_notification_id_notifications_notificationid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateField(help_text="Notification's arrived date.", null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='isRead',
            field=models.BooleanField(default=False, help_text="Notification's is readed by user or not.", null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='nType',
            field=models.CharField(blank=True, help_text="Notification's type.", max_length=255, null=True),
        ),
    ]
