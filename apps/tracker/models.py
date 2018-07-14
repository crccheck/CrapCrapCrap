from django.db import models
from django.utils import timezone


class Property(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)


class Product(models.Model):
    identifier = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()


class TrackPoint(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Well, should work for most currencies, sorry Unidad de Fomento
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency_code = models.CharField(
        max_length=3,
        default='USD',
        help_text='ISO4217 Currency Code')
    timestamp = models.DateTimeField(default=timezone.now)
