# Generated by Django 5.0.1 on 2024-02-20 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0005_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='description',
            new_name='content',
        ),
    ]
