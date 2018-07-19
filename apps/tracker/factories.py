import factory

from . import models


class PropertyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Property


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product
    property = factory.SubFactory(PropertyFactory)
    identifier = factory.Faker('license_plate')
    name = factory.Faker('name')


class TrackPointFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.TrackPoint
    product = factory.SubFactory(ProductFactory)
    price = '9.99'
