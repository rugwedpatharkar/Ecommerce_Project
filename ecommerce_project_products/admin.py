from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Brand, Category, Product, Review

class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand

@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    resource_class = BrandResource
    list_display = ('name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('created_at',)

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('category_name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)
    ordering = ('created_at',)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('title', 'category', 'brand', 'price', 'created_at', 'updated_at', 'stock', 'image')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'brand')
    search_fields = ('title', 'brand__name')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('popularity',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Fix for the issue with filtering by category__uid__exact
        if '__' in search_term:
            search_fields = self.get_search_fields(request)
            queryset |= self.get_advanced_search_results(request, queryset, search_term, search_fields)

        return queryset, use_distinct

    def get_advanced_search_results(self, request, queryset, search_term, search_fields):
        """
        Handle advanced search queries, e.g., filtering by related fields.
        """
        search_filters = {}
        for field_name in search_fields:
            if '__' in field_name:
                filter_name, lookup_expr = field_name.rsplit('__', 1)
                search_filters[field_name] = search_term
                queryset = queryset.filter(**search_filters)
        return queryset

class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review

@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = ReviewResource
    list_display = ('user', 'product', 'created_at', 'updated_at')
    list_filter = ('product',)
    search_fields = ('user__username', 'product__title')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
