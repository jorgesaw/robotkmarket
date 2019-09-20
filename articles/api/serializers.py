from rest_framework import serializers
from articles.models import Article, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'active')
        depth = 0

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Article
        fields = ('id', 'code', 'name', 'desc', 'price', 
                'stock', 'stock_min', 'stock_max', 'active', 'category')
        depth = 0
