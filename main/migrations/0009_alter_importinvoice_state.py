# Generated by Django 5.1.3 on 2024-11-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_stock_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importinvoice',
            name='state',
            field=models.CharField(choices=[('new', 'New'), ('accepted', 'Accepted'), ('canceled', 'Canceled')], default='new', max_length=10),
        ),
    ]
