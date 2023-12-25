from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_countries.fields import CountryField
from ecommerce_project_base.models import BaseModel
 

class Brand(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name

class Product(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True,max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    price = models.FloatField()
    product_description = models.TextField()
    image = models.ImageField(upload_to="product")
    is_active = models.BooleanField(default=True)
    popularity = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def update_popularity(self):
        self.popularity = Review.objects.filter(product=self).count()
        self.save()

    def is_in_stock(self):
        return self.stock > 0
    
    
class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} Review"
