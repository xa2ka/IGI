# Generated by Django 5.0.6 on 2024-09-09 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]