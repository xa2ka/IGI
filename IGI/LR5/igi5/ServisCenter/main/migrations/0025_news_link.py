# Generated by Django 5.0.6 on 2024-09-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_orderitem_supplierid'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]