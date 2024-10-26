# Generated by Django 5.1.2 on 2024-10-25 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0009_auto_20241025_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='StoreProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('kategori', models.CharField(max_length=200)),
                ('harga', models.IntegerField()),
                ('image', models.TextField()),
                ('toko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.store')),
            ],
        ),
    ]
