from django.db import models
from django.db import transaction
from django.contrib.auth.models import User

from utils.models_mixin import StatusCreatedUpdatedModelMixin
from locations.models import City
# Create your models here.

class AbstractPerson(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a person."""

    id_card = models.CharField(max_length=30, unique=True, verbose_name="CUIL/CUIT")
    first_name = models.CharField(max_length=210, verbose_name="Nombre")
    last_name = models.CharField(max_length=210, verbose_name="Apellido")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    desc = models.TextField(null=True, blank=True, verbose_name="Descripción")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")

    movile = models.CharField(max_length=50, null=True, blank=True, verbose_name="Celular")
    telephone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = "persona"
        verbose_name_plural = "personas"

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.full_name

class AbstractPersonWithCity(AbstractPerson):
    """Model representing a person with city."""

    city = models.ForeignKey(City, default=1, on_delete=models.SET_NULL, null=True, verbose_name='Ciudad')

    class Meta:
        abstract = True

class AbstractPersonUser(AbstractPerson):
    """Model representing a person with user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @transaction.atomic
    def save(self, *args, **kwargs):
        user = User(username=self.id_card)
        user.set_password(self.id_card)
        user.save()
        self.user = user
        super(AbstractPerson, self).save(*args, **kwargs)
