# Generated by Django 4.1.3 on 2022-11-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0018_alter_salesitems_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrecord',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salesitems',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
