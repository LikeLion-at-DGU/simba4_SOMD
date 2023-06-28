# Generated by Django 4.2.1 on 2023-06-21 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='somd',
            name='admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='somd_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='somd',
            name='admins',
            field=models.ManyToManyField(related_name='somd_admins', to=settings.AUTH_USER_MODEL),
        ),
    ]