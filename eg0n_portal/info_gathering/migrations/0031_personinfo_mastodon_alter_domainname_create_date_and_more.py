# Generated by Django 4.2.16 on 2024-12-19 21:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_gathering', '0030_alter_domainname_administrative_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personinfo',
            name='mastodon',
            field=models.CharField(blank=True, default='none', max_length=64),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 19, 21, 54, 36, 676059, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 19, 21, 54, 36, 676251, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 19, 21, 54, 36, 676247, tzinfo=datetime.timezone.utc)),
        ),
    ]
