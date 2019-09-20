from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import Article, Category, ArticleWithoutPrice
from .forms import ArticleForm, CategoryForm, ArticleWithoutPriceForm
from core.views import StaffRequiredMixin
# Create your views here.

class CategoryListView(ListView):
    model = Category
    paginate_by = 25

class CategoryDetailView(DetailView):
    model = Category

@method_decorator(staff_member_required, name='dispatch')
class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('articles:categories')

@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('articles:category-update', args=[self.object.id]) + "?ok"

@method_decorator(staff_member_required, name='dispatch')
class CategoryDelete(DeleteView):
    model = Category
    #success_url = reverse_lazy('articles:categories')

    def get_success_url(self):
        return reverse_lazy('articles:categories') + "?remove"

class ArticleListView(ListView):
    model = ArticleWithoutPrice
    paginate_by = 25

class ArticleDetailView(DetailView):
    model = ArticleWithoutPrice

@method_decorator(staff_member_required, name='dispatch')
class ArticleCreate(CreateView):
    model = ArticleWithoutPrice
    form_class = ArticleWithoutPriceForm
    success_url = reverse_lazy('articles:articles')

@method_decorator(staff_member_required, name='dispatch')
class ArticleUpdate(UpdateView):
    model = ArticleWithoutPrice
    form_class = ArticleWithoutPriceForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('articles:update', args=[self.object.id]) + "?ok"

@method_decorator(staff_member_required, name='dispatch')
class ArticleDelete(DeleteView):
    model = ArticleWithoutPrice
    success_url = reverse_lazy('articles:articles')
