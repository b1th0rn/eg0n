# Generated by Django 4.2.16 on 2024-12-14 10:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0023_ipadd_author_ipadd_lastchange_author_vuln_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipadd',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 14, 10, 56, 36, 218637, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='vulnreview',
            name='cve',
            field=models.ForeignKey(db_column='name', on_delete=django.db.models.deletion.CASCADE, to='ioc_management.vuln', to_field='name', unique=True),
        ),
    ]