# Generated by Django 4.2.16 on 2024-12-08 23:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0005_alter_ipadd_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipadd',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 8, 23, 35, 3, 657737, tzinfo=datetime.timezone.utc)),
        ),
    ]
