# Generated by Django 3.0.3 on 2020-03-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0005_auto_20200302_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='diagnosticsID',
        ),
        migrations.AddField(
            model_name='tasks',
            name='correlationID',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='tasks',
            name='diagnosticsid',
            field=models.CharField(default=0, max_length=100, primary_key=True, serialize=False),
        ),
    ]
