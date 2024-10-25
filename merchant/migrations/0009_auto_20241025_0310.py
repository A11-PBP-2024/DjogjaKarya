# Generated by Django 5.1.2 on 2024-10-25 03:10

from django.db import migrations
from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "stores.json")

class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0008_alter_store_address_alter_store_image1_and_more'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
