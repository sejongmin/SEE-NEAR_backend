# Generated by Django 4.2 on 2024-05-10 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('location', models.CharField(blank=True, max_length=32)),
                ('datetime', models.DateTimeField()),
                ('family_id', models.ForeignKey(db_column='family_id', on_delete=django.db.models.deletion.CASCADE, related_name='event', to='authentication.family')),
            ],
            options={
                'verbose_name': 'events',
                'verbose_name_plural': 'event',
                'ordering': ('id',),
            },
        ),
    ]
