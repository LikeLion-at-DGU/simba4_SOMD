# Generated by Django 4.2.1 on 2023-06-22 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_image_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='somd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.somd'),
            preserve_default=False,
        ),
    ]
