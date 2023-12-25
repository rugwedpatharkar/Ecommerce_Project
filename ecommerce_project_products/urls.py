# urls.py in your app

from django.urls import path
from .views import CategoryProductTypeListView, ProductDetailView, HomeView, add_review, category_list

urlpatterns = [
    path('category/<slug:category_slug>/', CategoryProductTypeListView.as_view(), name='category_product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_review/<slug:slug>/', add_review, name='add_review'),
    path('categories/', category_list, name='category_list'),

]

