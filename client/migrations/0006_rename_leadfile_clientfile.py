# Generated by Django 5.0.1 on 2024-02-20 12:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_leadfile'),
        ('team', '0004_team_plan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeadFile',
            new_name='ClientFile',
        ),
    ]