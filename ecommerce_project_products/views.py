from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import ListView, DetailView
from .models import Category, Product, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.db.models import Count, F
from django.db.models import Case, When, Value
from django.db.models import IntegerField
from django.views.generic import ListView


class CategoryProductTypeListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    page_kwarg = 'page'  # Add this line to match the query parameter

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=category, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context
        
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get related products based on the category of the current product
        related_products = Product.objects.filter(category=self.object.category).exclude(slug=self.object.slug)[:4]

        context['reviews'] = Review.objects.filter(product=self.object)
        context['category'] = self.object.category
        context['brand'] = self.object.brand
        context['related_products'] = related_products

        return context

@login_required
def add_review(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        text = request.POST.get('text')
        user = request.user  
        review = Review.objects.create(user=user, product=product, text=text)
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            file_name = f"review_images/{user.username}_{product.slug}_{image_file.name}"
            file_path = default_storage.save(file_name, ContentFile(image_file.read()))
            review.image.name = file_path
            review.save()

        return redirect('product_detail', slug=slug)

    return redirect('home')  # Redirect to home if not a POST request




class HomeView(ListView):
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'products'
    ordering = '-popularity'
    paginate_by = 10  # Set the number of items per page

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        # Show all active products in stock, order by popularity, and filter by category, product title, or brand
        products = Product.objects.filter(
            Q(category__category_name__icontains=query) |
            Q(title__icontains=query) |
            Q(brand__name__icontains=query),
            is_active=True,
            stock__gt=0
        ).annotate(
            total_reviews=Count('reviews'),
            weighted_popularity=F('popularity') + Case(
                When(total_reviews__gt=0, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-weighted_popularity')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add best seller products to context
        best_sellers = Product.objects.filter(is_active=True, stock__gt=0).order_by('-popularity')[:5]
        context['best_sellers'] = best_sellers

        return context
    

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})