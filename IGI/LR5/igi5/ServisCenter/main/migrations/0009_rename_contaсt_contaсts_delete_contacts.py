# Generated by Django 5.0.6 on 2024-05-23 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_contaсt_delete_mymodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contaсt',
            new_name='Contaсts',
        ),
        migrations.DeleteModel(
            name='Contacts',
        ),
    ]
