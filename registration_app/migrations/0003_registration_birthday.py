# Generated by Django 2.2 on 2021-05-22 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0002_registration_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='birthday',
            field=models.CharField(default='birthday', max_length=20),
        ),
    ]