# Generated by Django 4.1.3 on 2023-01-12 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0032_alter_inventoryrecord_st_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrecord',
            name='st_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
