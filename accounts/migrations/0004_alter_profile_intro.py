# Generated by Django 4.2.1 on 2023-06-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_email_profile_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='intro',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]