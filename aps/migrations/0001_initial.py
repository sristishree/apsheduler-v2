# Generated by Django 3.0.3 on 2020-02-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('coid', models.IntegerField(primary_key=True, serialize=False)),
                ('command', models.CharField(max_length=100)),
            ],
        ),
    ]