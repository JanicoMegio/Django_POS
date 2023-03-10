# Generated by Django 4.1.3 on 2022-11-22 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0021_remove_inventoryrecord_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryrecord',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.products'),
        ),
        migrations.AlterField(
            model_name='inventoryrecord',
            name='st_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
