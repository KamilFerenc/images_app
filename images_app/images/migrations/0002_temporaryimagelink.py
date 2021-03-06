# Generated by Django 3.1.3 on 2020-11-20 19:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryImageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_suffix', models.CharField(max_length=100, verbose_name='Link suffix')),
                ('time_expiration', models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(300),
                                django.core.validators.MaxValueValidator(30000)], verbose_name='Time expiration')),
                ('expire_at', models.DateTimeField(blank=True, null=True, verbose_name='Expire at')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.userimage',
                                                 verbose_name='User image')),
            ],
        ),
    ]
