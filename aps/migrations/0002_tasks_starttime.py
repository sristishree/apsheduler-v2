# Generated by Django 3.0.3 on 2020-02-20 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='starttime',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]