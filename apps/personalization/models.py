from django.conf import settings
from django.db import models


class List(models.Model):
    """A wishlist"""
    # https://stackoverflow.com/questions/3759006/generating-a-non-sequential-id-pk-for-a-django-model
    # TODO key = models.CharField(max_length=8, unique=True, default=pkgen)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lists')
    products = models.ManyToManyField(
        'tracker.Product', through='ListItem', related_name='lists')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} {self.name}'


class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    product = models.ForeignKey('tracker.Product', on_delete=models.CASCADE)
    order = models.IntegerField(default=0, help_text='Custom ordering')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('list', 'product')
        ordering = ('order',)
