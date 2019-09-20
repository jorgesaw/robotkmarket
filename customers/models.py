from django.db import models

from persons.models import AbstractPersonWithCity
# Create your models here.

class Customer(AbstractPersonWithCity):
    """Model representing a customer."""

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"