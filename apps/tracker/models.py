from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.personalization.models import pkgen


class Property(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(unique=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.name or self.url


class Product(models.Model):
    key = models.CharField(max_length=9, unique=True, default=pkgen)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='products')
    identifier = models.CharField(max_length=200, help_text='Some unique identifier for the product on the site (e.g. a SKU, product id, or URL)')
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    last_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    last_price_check = models.DateTimeField(null=True)
    min_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text='Cheapest price seen')
    price_base = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text='Highest price seen, typically the MSRP')
    price_drop_short = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text='The price drop over the short period, usually a day')
    price_drop_long = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text='The price drop over a long period, usually a week')

    class Meta:
        unique_together = ('property', 'identifier')

    def __str__(self):
        return self.name or self.identifier

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={'property_slug': self.property.slug, 'pk': self.pk})


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
