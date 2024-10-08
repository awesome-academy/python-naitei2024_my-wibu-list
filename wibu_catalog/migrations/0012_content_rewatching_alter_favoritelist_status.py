# Generated by Django 5.1 on 2024-08-27 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wibu_catalog', '0011_alter_content_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='reWatching',
            field=models.IntegerField(default=0, help_text='Re-Watching.', null=True),
        ),
        migrations.AlterField(
            model_name='favoritelist',
            name='status',
            field=models.CharField(choices=[(1, 'Watching'), (2, 'Completed'), (3, 'On Hold'), (4, 'Dropped'), (5, 'Re-Watching'), (6, 'Plan to Watch')], default='1', help_text='User status with this content.', max_length=1, null=True),
        ),
    ]
