# Generated by Django 3.0.3 on 2020-03-04 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0008_auto_20200303_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='correlationID',
        ),
    ]
