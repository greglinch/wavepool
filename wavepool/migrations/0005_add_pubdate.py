# Generated by Django 3.0.3 on 2020-02-29 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wavepool', '0004_add_instructions_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='publish_date',
            field=models.DateField(default=datetime.date(2020, 2, 29)),
        ),
    ]