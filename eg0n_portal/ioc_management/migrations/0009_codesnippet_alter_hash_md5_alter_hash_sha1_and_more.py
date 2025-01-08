# Generated by Django 5.1.4 on 2025-01-01 18:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0008_alter_hash_sha256_hashreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeSnippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='none', max_length=56, unique=True)),
                ('language', models.CharField(choices=[('cmd', 'cmd'), ('powershell', 'powershell'), ('bash', 'bash'), ('python', 'python')], default='python', max_length=16)),
                ('confidence', models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], default='low', max_length=16)),
                ('code', models.TextField()),
                ('description', models.TextField()),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('expire_date', models.DateField(default=django.utils.timezone.now)),
                ('author', models.CharField(default=None, editable=False, max_length=32)),
                ('lastchange_author', models.CharField(default=None, editable=False, max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='hash',
            name='md5',
            field=models.CharField(blank=True, default='none', max_length=32),
        ),
        migrations.AlterField(
            model_name='hash',
            name='sha1',
            field=models.CharField(blank=True, default='none', max_length=40),
        ),
        migrations.AlterField(
            model_name='hash',
            name='sha256',
            field=models.CharField(blank=True, default='none', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='hash',
            name='website',
            field=models.URLField(blank=True, default='none.sample', max_length=50),
        ),
        migrations.CreateModel(
            name='CodeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_name', models.CharField(default='none', max_length=64, unique=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('references_url', models.CharField(blank=True, max_length=256, null=True)),
                ('exploit_url', models.CharField(blank=True, max_length=256, null=True)),
                ('author', models.CharField(default=None, editable=False, max_length=32)),
                ('lastchange_author', models.CharField(default=None, editable=False, max_length=32)),
                ('code', models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, related_name='code_review', to='ioc_management.codesnippet', to_field='name')),
            ],
        ),
    ]
