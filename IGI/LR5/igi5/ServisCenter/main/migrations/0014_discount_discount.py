# Generated by Django 5.0.6 on 2024-05-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_news_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='Скидка'),
            preserve_default=False,
        ),
    ]
