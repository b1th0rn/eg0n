# Generated by Django 4.2.16 on 2024-12-22 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0002_alter_hash_expire_date_alter_ipadd_expire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hash',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 22, 20, 48, 16, 880715, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ipadd',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 22, 20, 48, 16, 880334, tzinfo=datetime.timezone.utc)),
        ),
    ]