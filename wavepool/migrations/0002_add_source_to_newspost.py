# Generated by Django 3.0.3 on 2020-02-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wavepool', '0001_init_newspost_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='source',
            field=models.URLField(default='http://industrydive.com'),
            preserve_default=False,
        ),
    ]