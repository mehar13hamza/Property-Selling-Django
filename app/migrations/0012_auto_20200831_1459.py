# Generated by Django 3.0.5 on 2020-08-31 09:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20200831_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='area',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='community',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='pets',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='price_per_area',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
