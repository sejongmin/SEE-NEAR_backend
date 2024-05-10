# Generated by Django 4.2 on 2024-05-01 05:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('start', models.TimeField(auto_now_add=True)),
                ('end', models.TimeField(auto_now=True)),
                ('keyword', models.CharField(blank=True, max_length=16)),
                ('emotion', models.IntegerField(null=True)),
                ('family_id', models.ForeignKey(db_column='family_id', on_delete=django.db.models.deletion.CASCADE, related_name='post', to='authentication.family')),
            ],
            options={
                'verbose_name': 'posts',
                'verbose_name_plural': 'post',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='DayReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion_rate', models.FloatField(default=0)),
                ('bad_rate', models.FloatField(default=0)),
                ('post_count', models.IntegerField(default=0)),
                ('emotion_1', models.IntegerField(default=0)),
                ('emotion_2', models.IntegerField(default=0)),
                ('emotion_3', models.IntegerField(default=0)),
                ('emotion_4', models.IntegerField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('keywords', models.TextField(default='')),
                ('family_id', models.ForeignKey(db_column='family_id', on_delete=django.db.models.deletion.CASCADE, related_name='day', to='authentication.family')),
            ],
            options={
                'verbose_name': 'reports',
                'verbose_name_plural': 'report',
                'ordering': ('id',),
            },
        ),
    ]
