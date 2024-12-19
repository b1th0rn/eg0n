# Generated by Django 4.2.16 on 2024-12-19 21:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0027_alter_ipadd_expire_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='hash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, default='none', max_length=56)),
                ('platform', models.CharField(choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('macOS', 'macOS')], default='Windows', max_length=16)),
                ('sha256', models.TextField()),
                ('sha1', models.TextField()),
                ('md5', models.TextField()),
                ('website', models.URLField(blank=True, default='none', max_length=50)),
                ('confidence', models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], default='low', max_length=16)),
                ('description', models.TextField()),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('expire_date', models.DateField(default=datetime.datetime(2024, 12, 19, 21, 54, 36, 677213, tzinfo=datetime.timezone.utc))),
                ('author', models.CharField(default=None, editable=False, max_length=32)),
                ('lastchange_author', models.CharField(default=None, editable=False, max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='ipadd',
            name='expire_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 19, 21, 54, 36, 677021, tzinfo=datetime.timezone.utc)),
        ),
    ]
