# Generated by Django 3.0.3 on 2020-03-04 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0011_auto_20200304_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='correlationID',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='diagnosticsid',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
