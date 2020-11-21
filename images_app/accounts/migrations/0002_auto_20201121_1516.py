# Generated by Django 3.1.3 on 2020-11-21 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('images', '0003_thumbnailsettings'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True, verbose_name='Title')),
                ('original_image', models.BooleanField(default=False,
                                                       help_text='If True, user will get link to original '
                                                                 'image in response',
                                                       verbose_name='Original image')),
                ('generate_temp_link', models.BooleanField(default=False,
                                                           help_text='If True, user will have option to '
                                                                     'generate temporary link',
                                                           verbose_name='Generate temporary link')),
                ('thumbnails', models.ManyToManyField(related_name='account_tiers', to='images.ThumbnailSettings',
                                                      verbose_name='Thumbnails')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='account_tier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.accounttier',
                                    verbose_name='Account tier'),
        ),
    ]
