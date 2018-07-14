import factory

from . import models


class PropertyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Property


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product


class TrackPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.TrackPoint
    property = factory.SubFactory(PropertyFactory)
    product = factory.SubFactory(ProductFactory)
    price = '9.99'
