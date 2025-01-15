# Generated by Django 4.2.16 on 2024-12-29 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0006_alter_hash_expire_date_alter_ipadd_expire_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpAddReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_name', models.CharField(default='none', max_length=64, unique=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('author', models.CharField(default=None, editable=False, max_length=32)),
                ('lastchange_author', models.CharField(default=None, editable=False, max_length=32)),
                ('ip', models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, related_name='ip', to='ioc_management.ipadd', to_field='ip_address')),
            ],
        ),
    ]
