# Generated by Django 4.1.3 on 2022-11-21 12:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0020_alter_salesitems_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryrecord',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='salesitems',
            name='date_added',
        ),
        migrations.AddField(
            model_name='inventoryrecord',
            name='st_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salesitems',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
