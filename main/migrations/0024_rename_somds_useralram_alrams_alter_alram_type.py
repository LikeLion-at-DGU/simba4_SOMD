# Generated by Django 4.2.1 on 2023-06-25 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alram_useralram'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useralram',
            old_name='somds',
            new_name='alrams',
        ),
        migrations.AlterField(
            model_name='alram',
            name='type',
            field=models.TextField(),
        ),
    ]
