# Generated by Django 4.1.7 on 2023-03-04 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_login',
            field=models.DateTimeField(verbose_name='00:0:0:0'),
        ),
    ]