# Generated by Django 5.0.7 on 2024-07-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoyageApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]