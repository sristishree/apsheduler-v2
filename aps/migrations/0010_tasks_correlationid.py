# Generated by Django 3.0.3 on 2020-03-04 07:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0009_remove_tasks_correlationid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='correlationID',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]
