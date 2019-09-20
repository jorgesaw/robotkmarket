from django.db import models
from django.core.management import call_command
from django.db import transaction

import sys

from sales.models import Sale
from overheads.models import Overhead

# Create your models here.

class BackUp(models.Model):
    """Model representing a many to many relationship of backup."""

    created = models.DateField(auto_now_add=True, verbose_name="Fecha de creación")
    desc = models.CharField(max_length=255, verbose_name="Descripción")

    class Meta:
        ordering = ['id',]
        verbose_name = "backup"
        verbose_name_plural = "backups"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(BackUp, self).save(*args, **kwargs)

        date_created = str(self.created)
        file = 'C:\\bck\\db_{}_bck.json'.format(date_created)
        sysout = sys.stdout
        try:
            sys.stdout = open(file, 'w')
            call_command('dumpdata', 
                        '--exclude', 'auth.permission', 
                        '--exclude', 'admin.LogEntry', 
                        '--exclude', 'contenttypes',
                        '--exclude', 'sessions',  
                        '--indent', '4')
        except IOError:
            pass
        except:
            pass
        finally:
            sys.stdout.close()

        sys.stdout = sysout
        
        
        month = self.created.month
        year = self.created.year
        if month <=1: # Si es el primer mes del año tenemos que tomar la fecha del año anterior
            month = 12 
            year -= 1

        Sale.objects.filter(date_sale__year__lte=year, 
                                    date_sale__month__lt=month).delete()
        Overhead.objects.filter(date_overhead__year__lte=year, 
                                    date_overhead__month__lt=month).delete()

    def __str__(self):
        return str(self.created)