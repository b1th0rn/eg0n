# Generated by Django 5.1.4 on 2025-01-08 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ioc_management', '0010_merge_20250108_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codereview',
            old_name='code',
            new_name='code_review',
        ),
    ]
