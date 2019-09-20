from django.db import models
from django.db.models import Sum, F, FloatField, Max 
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import datetime
from decimal import Decimal

from customers.models import Customer
from articles.models import Article, PriceWithDesc
from utils.models_mixin import StatusCreatedUpdatedModelMixin
from .managers import SaleManager
# Create your models here.

TAX_CHOICES = [
    ("0", 0.0), 
    ("1", 0.21), 
    ("2", 0.105), 
]

ANONIMUS_CUSTOMER = 1
class Sale(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a category of sale."""

    number_sale = models.CharField(default='XXXX-XXXXXX', max_length=18, verbose_name="Número")
    date_sale = models.DateField(default=timezone.now, verbose_name="Fecha")
    discount = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, default=0)
    fiscal_bill = models.BooleanField(default=False, verbose_name="AFIP")
    tax = models.CharField(max_length=2, choices=TAX_CHOICES, default="0", verbose_name="IVA")
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="TOTAL")
    customer = models.ForeignKey(Customer, null=True, blank=True, default=ANONIMUS_CUSTOMER, on_delete=models.SET_NULL, verbose_name="Cliente")

    objects = SaleManager()

    def calculate_total(self):
        tot = self.itemsale_set.all().aggregate(
            tot_sale=Sum( ( F('quantity') * F('article_price__value') ) - F('discount'), output_field=FloatField() ) # DEvuelve un diccionario con un dato cuya key es 'tot_sale' 
        )['tot_sale'] or 0

        tot = tot - float(self.discount)
        self.value = tot
        #self.save()
        Sale.objects.filter(id=self.id).update(value=tot)

    class Meta:
        ordering = ['id',]
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    def __str__(self):
        return self.number_sale

class SaleSummary(Sale):
    class Meta:
        proxy = True
        verbose_name = 'reporte venta'
        verbose_name_plural = 'reporte de ventas'
    
class ItemSale(models.Model):
    """Model representing a many to many relationship of sales and articles (item of sale)."""

    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    value = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, verbose_name="Total")
    discount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, verbose_name="Descuento")
    article_price = models.ForeignKey(PriceWithDesc, on_delete=models.CASCADE, verbose_name="Artículo")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Venta")

    class Meta:
        ordering = ['id',]
        verbose_name = "item"
        verbose_name_plural = "items"

    @property
    def actual_price(self):
        price = 0.0
        if self.article_price:
            price = self.article_price.value
        return price

    def calculate_total(self):
        price = self.article_price.value
        self.value = price * Decimal.from_float(self.quantity)
        
        stock = self.article_price.article.stock
        if stock and stock >= self.quantity * 2: 
            stock -= self.quantity * 2
            self.article_price.article.stock = stock
            self.article_price.article.save(update_fields=['stock',])
        
        return self.value

    def save(self, *args, **kwargs):
        super(ItemSale, self).save(*args, **kwargs)
        self.calculate_total()
        
        super(ItemSale, self).save(update_fields=['value'])

    def delete(self, *args, **kwargs):
        sale = self.sale
        article = self.article_price.article
        quantity = self.quantity

        super(ItemSale, self).delete(*args, **kwargs)
        sale.calculate_total()

        stock = article.stock
        stock += quantity
        article.stock = stock
        article.save(update_fields=['stock',])

    def __str__(self):
        return str(self.value)

class ItemSaleWithPrice(ItemSale):
    price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)

@receiver(post_save, sender=ItemSale)
def update_total_sales_at_item(sender, instance, **kwargs):
    instance.sale.calculate_total()

@receiver(pre_save, sender=ItemSale)
def update_stock_in_article(sender, instance, **kwargs):
    try:
        old_instance = ItemSale.objects.get(id=instance.id)
    except ItemSale.DoesNotExist:
        old_instance = None

    if not old_instance:
        return

    old_stock = old_instance.quantity

    if old_instance.article_price.article.stock:
        old_instance.article_price.article.stock += old_stock
        old_instance.article_price.article.save(update_fields=['stock',])

@receiver(post_save, sender=Sale)
def update_vendas_total(sender, instance, **kwargs):
    instance.calculate_total()
