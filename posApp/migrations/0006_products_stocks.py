# Generated by Django 3.0.14 on 2022-06-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0005_auto_20220609_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stocks',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
