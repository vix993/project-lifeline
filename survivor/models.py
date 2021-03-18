from django.db import models

from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MinLengthValidator
from .validators import Validation

from rest_framework.reverse import reverse as api_reverse

# This model is made for the purpose of storage.
# The survivors will have their details stored and validates.

class Survivor(models.Model):
    name = models.CharField(
        max_length=120, blank=False, default=None,
        validators=[MinLengthValidator(2), Validation().validate_name]
    )
    age = models.DecimalField(
        max_digits=3, decimal_places=0, blank=False, default=None,
        validators=[MinValueValidator(0)]
    )
    gender = models.CharField(
        max_length=1, blank=False, default=None,
        validators=[MinLengthValidator(1), Validation().validate_gender]
    )
    latitude = models.DecimalField(
        max_digits=12, decimal_places=10, default=None, blank=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    longitude = models.DecimalField(
        max_digits=12, decimal_places=10,
        default=None, blank=False,
        validators=[MaxValueValidator(90), MinValueValidator(-90)]
    )
    items = models.CharField(
        max_length=120, default=None,
        validators=[MinLengthValidator(1), Validation().validate_item]
    )
    infected = models.BooleanField(default=False)
    infection_marks = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("api-survivor:ru-survivor", kwargs={'pk': self.pk}, request=request)

    def get_api_url(self, request=None):
        return api_reverse("api-survivor:ru-survivor", kwargs={'pk': self.pk}, request=request)

class FlagAsInfected(models.Model):
    flaged_pk = models.CharField(max_length=120, blank=False, validators=[Validation().validate_pk])
    flager_pk = models.CharField(max_length=120, blank=False, validators=[Validation().validate_pk])

    def __str__(self):
        return str(self.flager_pk)
    
    def get_absolute_url(self):
        return reverse("api-survivor:flag-create", kwargs={'pk': self.pk}, request=request)
    
    def get_api_url(self, request=None):
        return api_reverse("api-survivor:flag-create", kwargs={'pk': self.pk}, request=request)

class TradeItem(models.Model):
    buyer_pk = models.DecimalField(max_digits=10, decimal_places=0,
                                   validators=[MinValueValidator(1)])
    seller_pk = models.DecimalField(max_digits=10, decimal_places=0,
                                    validators=[MinValueValidator(1)])
    offered_items = models.CharField(max_length=120, validators=[Validation().validate_item])
    requested_items = models.CharField(max_length=120, validators=[Validation().validate_item])

    def __str__(self):
        return self.buyer_pk

    def validate_offered_items(self):
        print(self.offered_items)

    def get_absolute_url(self):
        return reverse("api-survivor:trade-request", kwargs={'pk': self.pk}, request=request)