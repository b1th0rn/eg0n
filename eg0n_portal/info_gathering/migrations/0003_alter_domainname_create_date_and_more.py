# Generated by Django 4.2.16 on 2024-12-08 16:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_gathering', '0002_alter_domainname_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainname',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 8, 16, 38, 51, 388076, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 8, 16, 38, 51, 388086, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='organization_name',
            field=models.ForeignKey(db_column='organization_name', default='none', null=True, on_delete=django.db.models.deletion.CASCADE, to='info_gathering.organizationinfo', to_field='organization_name'),
        ),
        migrations.AlterField(
            model_name='domainname',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 8, 16, 38, 51, 388082, tzinfo=datetime.timezone.utc)),
        ),
    ]