# Generated by Django 4.2.16 on 2024-12-11 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_gathering', '0019_alter_domainname_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainname',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 25, 10, 818036, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 25, 10, 818054, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 11, 15, 25, 10, 818042, tzinfo=datetime.timezone.utc)),
        ),
    ]