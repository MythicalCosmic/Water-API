# Generated by Django 5.1.3 on 2024-11-23 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_stock_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='stock',
        ),
    ]