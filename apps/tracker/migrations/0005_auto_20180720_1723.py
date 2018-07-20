# Generated by Django 2.0.7 on 2018-07-20 17:23

from django.db import migrations

from apps.personalization.models import pkgen


def gen_key(apps, schema_editor):
    MyModel = apps.get_model('tracker', 'Product')
    for row in MyModel.objects.all():
        row.key = pkgen()
        row.save(update_fields=['key'])


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_auto_20180720_1711'),
    ]

    operations = [
        migrations.RunPython(gen_key, reverse_code=migrations.RunPython.noop),
    ]