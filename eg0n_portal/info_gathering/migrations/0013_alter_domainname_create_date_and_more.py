# Generated by Django 4.2.16 on 2024-12-11 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_gathering', '0012_alter_domainname_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainname',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 8, 3, 27721, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 8, 3, 27730, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 8, 3, 27726, tzinfo=datetime.timezone.utc)),
        ),
    ]
