# Generated by Django 4.2 on 2024-04-17 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_family_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='id',
            field=models.CharField(default='14483B0', editable=False, max_length=6, primary_key=True, serialize=False),
        ),
    ]
