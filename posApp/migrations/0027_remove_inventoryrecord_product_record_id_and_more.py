# Generated by Django 4.1.3 on 2022-11-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0026_alter_inventoryrecord_product_record_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryrecord',
            name='product_record_id',
        ),
        migrations.AddField(
            model_name='inventoryrecord',
            name='product_name',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
