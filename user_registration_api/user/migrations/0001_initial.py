# Generated by Django 4.1.7 on 2023-03-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('userId', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=355)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=255)),
                ('age', models.IntegerField()),
                ('height_cm', models.FloatField()),
                ('weight_kg', models.FloatField()),
                ('calculated_BMI', models.FloatField(default=0.0)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(null=True)),
                ('session_token', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
