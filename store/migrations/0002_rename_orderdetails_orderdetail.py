# Generated by Django 5.1 on 2024-08-12 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderDetails',
            new_name='OrderDetail',
        ),
    ]
