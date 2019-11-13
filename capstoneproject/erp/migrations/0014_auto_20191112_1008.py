# Generated by Django 2.2.5 on 2019-11-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0013_auto_20191111_0519'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Order Detail',
                'verbose_name_plural': 'Order Details',
                'db_table': 'OrderItem',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='OrderDetail',
        ),
    ]