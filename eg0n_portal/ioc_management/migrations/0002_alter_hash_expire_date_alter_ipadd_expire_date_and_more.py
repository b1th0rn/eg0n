# Generated by Django 4.2.16 on 2024-12-22 20:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hash',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 22, 20, 46, 28, 902772, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ipadd',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 22, 20, 46, 28, 902558, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='vulnreview',
            name='cve_name',
            field=models.OneToOneField(db_column='name', default='none', on_delete=django.db.models.deletion.CASCADE, related_name='cve_name', to='ioc_management.vuln', to_field='name'),
        ),
    ]