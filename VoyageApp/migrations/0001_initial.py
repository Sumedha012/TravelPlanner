# Generated by Django 5.0.7 on 2024-07-10 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Beach', 'Beach'), ('Mountain', 'Mountain'), ('Desert', 'Desert'), ('Wildlife', 'Wildlife/Forest'), ('Historical', 'Historical/Monuments'), ('Temple', 'Temples/Pilgrimage'), ('Botanical', 'Botanical Garden'), ('Adventure', 'Adventure Sports'), ('Wellness', 'Wellness and Luxury'), ('City', 'City - Shopping, Nightlife'), ('Festival', 'Festival/Cultural'), ('Other', 'Others')], max_length=50)),
                ('budget', models.CharField(choices=[('Low', 'Low'), ('Mid', 'Mid'), ('High', 'High')], max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_type', models.CharField(choices=[('Beach', 'Beach'), ('Mountain', 'Mountain'), ('Desert', 'Desert'), ('Wildlife', 'Wildlife/Forest'), ('Historical', 'Historical/Monuments'), ('Temple', 'Temples/Pilgrimage'), ('Botanical', 'Botanical Garden'), ('Adventure', 'Adventure Sports'), ('Wellness', 'Wellness and Luxury'), ('City', 'City - Shopping, Nightlife'), ('Festival', 'Festival/Cultural'), ('Other', 'Others')], max_length=50)),
                ('budget', models.CharField(choices=[('Low', 'Low'), ('Mid', 'Mid'), ('High', 'High')], max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
    ]
