from django.db import models
from django.urls import reverse_lazy

from utils.models_mixin import StatusCreatedUpdatedModelMixin
# Create your models here.

class AbstractCategory(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a category of article."""
    name = models.CharField(max_length=150, verbose_name="Nombre")

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return ""#reverse_lazy('category-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.name

class Category(AbstractCategory):
    pass

class AbstractArticleWithoutPrice(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a product."""
    code = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name="Código")
    name = models.CharField(max_length=210, verbose_name="Nombre")
    desc = models.CharField(max_length=255, verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    stock_min = models.PositiveIntegerField(null=True, blank=True, verbose_name="Stock mínimo")
    stock_max = models.PositiveIntegerField(null=True, blank=True, verbose_name="Stock máximo")
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name="Imagen")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def get_absolute_url(self):
        """Returns the url to access a particular article instance."""
        return ""#reverse_lazy('article-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.name)

class AbstractArticle(AbstractArticleWithoutPrice):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")

class Article(AbstractArticle):
    pass

class ArticleWithoutPrice(AbstractArticleWithoutPrice):
    class Meta:
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

class Price(models.Model):
    """Model representing a price."""
    value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Valor")

    class Meta:
        ordering = ['id']
        verbose_name = "precio"
        verbose_name_plural = "precios"

    def get_absolute_url(self):
        """Returns the url to access a particular article instance."""
        return ""#reverse_lazy('article-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.value)


class PriceWithDesc(Price):
    """Model representing a price."""
    desc = models.CharField(max_length=210, verbose_name="Tipo de precio")

    article = models.ForeignKey(ArticleWithoutPrice, on_delete=models.CASCADE)

    class Meta:
        ordering = ['desc']
        verbose_name = 'precio con descripcion'
        verbose_name_plural = 'precios con descripcion'

    def save(self, *args, **kwargs):
        desc = self.desc
        self.desc = self.article.name + ' ' + desc
        super(PriceWithDesc, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - $ {}'.format(self.article.name, self.desc, self.value)
