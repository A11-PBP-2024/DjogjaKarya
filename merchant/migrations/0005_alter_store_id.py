# Generated by Django 5.1.2 on 2024-10-23 06:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0004_remove_store_image_store_image1_store_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]