# Generated by Django 4.2.1 on 2023-06-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='intro',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]