# Generated by Django 4.2.16 on 2024-12-22 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infosec_dashboard', '0002_alter_asset_end_of_life'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='end_of_life',
            field=models.DateField(default=datetime.datetime(2024, 12, 22, 20, 48, 16, 881033, tzinfo=datetime.timezone.utc)),
        ),
    ]
