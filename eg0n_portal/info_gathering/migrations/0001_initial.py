# Generated by Django 4.2.16 on 2024-12-22 20:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=64, unique=True)),
                ('organization_address', models.CharField(blank=True, default='none', max_length=64)),
                ('organization_coordinates', models.CharField(blank=True, default='none', max_length=64)),
                ('url', models.CharField(blank=True, default='none', max_length=64)),
                ('description', models.TextField()),
                ('publish_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('address', models.CharField(blank=True, default='none', max_length=64)),
                ('coordinates', models.CharField(blank=True, default='none', max_length=64)),
                ('email', models.CharField(blank=True, default='none', max_length=64)),
                ('mobile', models.CharField(blank=True, default='none', max_length=64)),
                ('website', models.CharField(blank=True, default='none', max_length=64)),
                ('linkedin', models.CharField(blank=True, default='none', max_length=64)),
                ('facebook', models.CharField(blank=True, default='none', max_length=64)),
                ('instagram', models.CharField(blank=True, default='none', max_length=64)),
                ('tiktok', models.CharField(blank=True, default='none', max_length=64)),
                ('mastodon', models.CharField(blank=True, default='none', max_length=64)),
                ('description', models.TextField()),
                ('publish_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=64, unique=True)),
                ('name_server_1', models.CharField(blank=True, default='none', max_length=64)),
                ('name_server_2', models.CharField(blank=True, default='none', max_length=64)),
                ('name_server_3', models.CharField(blank=True, default='none', max_length=64)),
                ('description', models.TextField()),
                ('create_date', models.DateField(default=datetime.datetime(2024, 12, 22, 20, 43, 53, 879310, tzinfo=datetime.timezone.utc))),
                ('update_date', models.DateField(default=datetime.datetime(2024, 12, 22, 20, 43, 53, 879550, tzinfo=datetime.timezone.utc))),
                ('expire_date', models.DateField(default=datetime.datetime(2024, 12, 22, 20, 43, 53, 879555, tzinfo=datetime.timezone.utc))),
                ('administrative_contact', models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, related_name='administrative', to='info_gathering.personinfo', to_field='name')),
                ('organization_name', models.ForeignKey(db_column='organization_name', default='none', null=True, on_delete=django.db.models.deletion.CASCADE, to='info_gathering.organizationinfo', to_field='organization_name')),
                ('technical_contact', models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, related_name='technical', to='info_gathering.personinfo', to_field='name')),
            ],
        ),
    ]
