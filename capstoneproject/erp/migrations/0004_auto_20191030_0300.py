# Generated by Django 2.2.5 on 2019-10-30 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_auto_20191019_0439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'managed': False, 'ordering': ['acct_type']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'managed': False, 'ordering': ['title', 'emp_id']},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'managed': False, 'ordering': ['make']},
        ),
    ]
