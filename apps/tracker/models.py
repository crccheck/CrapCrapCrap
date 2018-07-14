from django.db import models
from django.utils import timezone


class Property(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name or self.url


class Product(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='products')
    identifier = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    # TODO description
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name or self.identifier


class TrackPoint(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    # Well, 2 decimal places should work for most, sorry Unidad de Fomento
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency_code = models.CharField(
        max_length=3,
        default='USD',
        help_text='ISO4217 Currency Code')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # TODO use localization
        return '%s %s $%s' % (self.property, self.product, self.price)
