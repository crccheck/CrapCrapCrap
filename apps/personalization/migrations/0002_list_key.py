# Generated by Django 2.0.7 on 2018-07-20 17:06

import apps.personalization.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personalization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='key',
            field=models.CharField(default=apps.personalization.models.pkgen, max_length=9, unique=True),
        ),
    ]
