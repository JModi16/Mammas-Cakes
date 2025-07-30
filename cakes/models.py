from django.db import models

class Cake(models.Model):
    CATEGORY_CHOICES = [
        ('birthday', 'Birthday Cakes'),
        ('wedding', 'Wedding Cakes'),
        ('treat', 'Treats'),
        ('vegan', 'Vegan Cakes'),
        ('all', 'All Cakes & Treats'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='cakes/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name