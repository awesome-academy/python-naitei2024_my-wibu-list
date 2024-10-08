# Generated by Django 3.2.25 on 2024-08-13 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wibu_catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('UID', models.IntegerField(help_text='User id', primary_key=True, serialize=False)),
                ('Username', models.CharField(help_text='Username', max_length=255, null=True)),
                ('Role', models.CharField(choices=[('admin', 'admin'), ('new_user', 'new_user'), ('longtime_user', 'longtime_user'), ('user', 'user'), ('VIP', 'VIP')], default='new_user', help_text='User role.', max_length=20, null=True)),
                ('Email', models.CharField(help_text='Email address', max_length=255, null=True)),
                ('Password', models.CharField(help_text='Password', max_length=255, null=True)),
                ('Date_of_birth', models.DateField(blank=True, help_text='Date of birth', null=True)),
                ('Profile_picture', models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to='')),
                ('Registration_date', models.DateField(help_text="Account's registration date", null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='comments',
            name='Content',
            field=models.TextField(help_text="User's comment.", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='Date_of_cmt',
            field=models.DateField(blank=True, help_text="Comment's date.", null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='Likes',
            field=models.IntegerField(default=0, help_text='Number of likes.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Aired',
            field=models.CharField(blank=True, help_text='Publish date.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Category',
            field=models.CharField(choices=[(1, 'Anime'), (2, 'Manga')], default='anime', help_text='Content category', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Completed',
            field=models.IntegerField(default=0, help_text='Completed.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Ctype',
            field=models.CharField(blank=True, help_text='Manga type (Oneshot, shounen,...)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Dropped',
            field=models.IntegerField(default=0, help_text='Dropped.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Duration',
            field=models.CharField(blank=True, help_text='None for Manga.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Episodes',
            field=models.IntegerField(blank=True, help_text='Number of published chapters.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Favorites',
            field=models.IntegerField(default=0, help_text='Number of user have this manga in their favorite list.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Genres',
            field=models.CharField(blank=True, help_text="Content's Genres", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Last_update',
            field=models.DateField(blank=True, help_text='Date of last published chapter.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Licensors',
            field=models.CharField(blank=True, help_text='Companies that have the rights to translate, publish, and distribute the manga.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Name',
            field=models.CharField(help_text='Content name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='On_Hold',
            field=models.IntegerField(default=0, help_text='On Hold.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Picture',
            field=models.ImageField(blank=True, default=None, help_text='Content cover picture.', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='content',
            name='Plan_to_Watch',
            field=models.IntegerField(default=0, help_text='Plan to Read.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Producers',
            field=models.CharField(blank=True, help_text='None for Manga.', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Ranked',
            field=models.IntegerField(default=0, help_text='.', null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Rating',
            field=models.CharField(blank=True, help_text='Manga age rate (e.g. safe).', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Score_avg',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Source',
            field=models.CharField(blank=True, help_text='Light novel, Book, etc. (e.g Original).', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Studios',
            field=models.CharField(blank=True, help_text='Tteams that assist the main artist with tasks.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='Watching',
            field=models.IntegerField(default=0, help_text='Reading.', null=True),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='Progress',
            field=models.IntegerField(default='0', help_text="User's progress (e.g. chapter01).", null=True),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='Status',
            field=models.CharField(choices=[(1, 'Watching'), (2, 'Completed'), (3, 'On_Hold'), (4, 'Dropped'), (5, 'Re_Watching'), (6, 'Plan_to_Watch')], default='1', help_text='User status with this content.', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='Cmt',
            field=models.TextField(blank=True, help_text='User comment about the product.', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='Rate',
            field=models.IntegerField(blank=True, help_text='User rating of the product.', null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='Message',
            field=models.TextField(help_text="Notification's message.", max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='Ntype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='Order_date',
            field=models.DateField(help_text='Date of the order.', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='Status',
            field=models.CharField(help_text='Order status (e.g. Shipped).', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='Buy_price',
            field=models.FloatField(help_text='Price at the time of Ordered.', null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='Quantity',
            field=models.IntegerField(default=1, help_text='Number of ordered products.', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.TextField(blank=True, help_text="Product's description.", max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Name',
            field=models.CharField(help_text='Name of the product.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Picture',
            field=models.ImageField(blank=True, help_text="Product's picture.", null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='Price',
            field=models.FloatField(default=0, help_text="Product's price.", null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Ravg',
            field=models.FloatField(default=0, help_text="Product's average rating.", null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_1',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_10',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_2',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_3',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_4',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_5',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_6',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_7',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_8',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='Score_9',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='score_list',
            name='Score',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default='10', help_text="User's score of this content.", null=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='wibu_catalog.users'),
        ),
        migrations.AlterField(
            model_name='favorite_list',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favlist', to='wibu_catalog.users'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='wibu_catalog.users'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='wibu_catalog.users'),
        ),
        migrations.AlterField(
            model_name='order',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='wibu_catalog.users'),
        ),
        migrations.AlterField(
            model_name='score_list',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoreslist', to='wibu_catalog.users'),
        ),
        migrations.DeleteModel(
            name='user',
        ),
    ]
