# Generated by Django 4.2.9 on 2024-03-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outfitted', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
