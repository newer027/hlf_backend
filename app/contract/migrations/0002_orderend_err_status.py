# Generated by Django 2.2 on 2019-09-23 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderend',
            name='err_status',
            field=models.BooleanField(default=False),
        ),
    ]
