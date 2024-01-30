# Generated by Django 4.2.9 on 2024-01-30 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outfitted', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(auto_created=True, default='0a443', editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.UUIDField(auto_created=True, default='5e30a', editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='productid',
            field=models.UUIDField(auto_created=True, default='28efd8', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]