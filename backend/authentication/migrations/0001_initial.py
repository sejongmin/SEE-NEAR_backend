# Generated by Django 4.2 on 2024-04-09 08:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_senior', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('birth', models.DateField(null=True)),
                ('role', models.CharField(max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.CharField(default='CDDB4EE', editable=False, max_length=6, primary_key=True, serialize=False)),
                ('family_name', models.CharField(default='new family', max_length=32)),
                ('senior_birth', models.DateField(null=True)),
                ('senior_gender', models.CharField(choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')], default=0, max_length=8)),
                ('senior_diseases', models.CharField(blank=True, max_length=128)),
                ('senior_interests', models.CharField(blank=True, max_length=128)),
                ('morning', models.TimeField(null=True)),
                ('evening', models.TimeField(null=True)),
                ('breakfast', models.TimeField(null=True)),
                ('lunch', models.TimeField(null=True)),
                ('dinner', models.TimeField(null=True)),
                ('senior_id', models.ForeignKey(db_column='senior_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='senior', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'family',
                'verbose_name_plural': 'familes',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='user',
            name='family_id',
            field=models.ForeignKey(db_column='family_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='family', to='authentication.family'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
