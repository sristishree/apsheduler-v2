# Generated by Django 3.0.3 on 2020-02-23 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aps', '0003_auto_20200220_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='interval',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='tasks',
            name='jobtype',
            field=models.CharField(default='interval', max_length=30),
            preserve_default=False,
        ),
    ]
