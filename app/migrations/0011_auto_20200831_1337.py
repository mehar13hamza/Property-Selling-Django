# Generated by Django 3.0.5 on 2020-08-31 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200831_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='address',
            field=models.TextField(default='123 block a dha'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='company',
            field=models.CharField(default='code genesis', max_length=150),
            preserve_default=False,
        ),
    ]
