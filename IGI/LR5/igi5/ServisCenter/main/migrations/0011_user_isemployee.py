# Generated by Django 5.0.6 on 2024-05-23 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_contaсts_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='IsEmployee',
            field=models.BooleanField(default=1, verbose_name='Сотрудник/Пользователь'),
            preserve_default=False,
        ),
    ]