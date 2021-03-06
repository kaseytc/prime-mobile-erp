# Generated by Django 2.2.5 on 2019-11-02 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('erp', '0004_auto_20191030_0300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'managed': False, 'ordering': ['lname', 'fname', 'cust_id']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'managed': False, 'ordering': ['title', 'lname', 'fname', 'emp_id']},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'managed': False, 'ordering': ['make', 'model']},
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='erp.Employee')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
