# Generated by Django 2.0.7 on 2018-07-20 17:23

from django.db import migrations, models

import apps.personalization.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20180720_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='key',
            field=models.CharField(default=apps.personalization.models.pkgen, max_length=9, unique=True),
        ),
    ]
