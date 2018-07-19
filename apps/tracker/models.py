from django.db import models
from django.utils import timezone


class Property(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(unique=True)

    class Meta:
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.name or self.url


class Product(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='products')
    identifier = models.CharField(max_length=200)
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    last_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    last_price_check = models.DateTimeField(null=True)
    price_drop_day = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    price_drop_week = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        unique_together = ('property', 'identifier')

    def __str__(self):
        return self.name or self.identifier


class TrackPoint(models.Model):
    CURRENCY_CODE_CHOICES = (
        ('USD', 'USD'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prices',
        editable=False)
    # Well, 2 decimal places should work for most, sorry Unidad de Fomento
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency_code = models.CharField(
        max_length=3,
        choices=CURRENCY_CODE_CHOICES,
        default='USD',
        help_text='ISO4217 Currency Code')
    timestamp = models.DateTimeField(default=timezone.now)
    compacted = models.BooleanField(default=False)

    def __str__(self):
        # TODO use localization
        return '%s $%s' % (self.product, self.price)
