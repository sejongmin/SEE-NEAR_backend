# Generated by Django 4.2 on 2024-04-17 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0004_alter_post_date_alter_report_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 17, 9, 9, 27, 294395, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 17, 9, 9, 27, 298627, tzinfo=datetime.timezone.utc)),
        ),
    ]
