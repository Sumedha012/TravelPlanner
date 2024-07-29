
from django.db import models

class Destination(models.Model):
    TYPE_CHOICES = [
        ('Beach', 'Beach'),
        ('Mountain', 'Mountain'),
        ('Desert', 'Desert'),
        ('Wildlife', 'Wildlife/Forest'),
        ('Historical', 'Historical/Monuments'),
        ('Temple', 'Temples/Pilgrimage'),
        ('Botanical', 'Botanical Garden'),
        ('Adventure', 'Adventure Sports'),
        ('Wellness', 'Wellness and Luxury'),
        ('City', 'City - Shopping, Nightlife'),
        ('Festival', 'Festival/Cultural'),
        ('Other', 'Others')
    ]

    BUDGET_CHOICES = [
        ('Low', 'Low'),
        ('Mid', 'Mid'),
        ('High', 'High')
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    # place_id = models.CharField(max_length=255, primary_key=True)  # Add this line

    def _str_(self):
        return self.name


class UserPreference(models.Model):
    BUDGET_CHOICES = [
        ('Low', 'Low'),
        ('Mid', 'Mid'),
        ('High', 'High')
    ]

    destination_type = models.CharField(max_length=50, choices=Destination.TYPE_CHOICES)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def _str_(self):
        return f"{self.destination_type} - {self.budget}"
