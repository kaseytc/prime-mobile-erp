# Generated by Django 2.2.5 on 2019-11-06 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_auto_20191102_2321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'managed': False, 'ordering': ['status', 'order_id']},
        ),
    ]