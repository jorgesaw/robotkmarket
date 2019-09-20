from django.urls import path, include
from . import views

articles_patterns = ([ 
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('categories/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category-delete'), 
    
    path('', views.ArticleListView.as_view(), name='articles'),
    path('<int:pk>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('create/', views.ArticleCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.ArticleUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDelete.as_view(), name='delete'),

    path('api/', include('articles.api.urls')), 
], 'articles')