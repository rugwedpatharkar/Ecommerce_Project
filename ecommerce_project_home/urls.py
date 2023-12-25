from django.urls import path
from ecommerce_project_products.views import HomeView  # Assuming HomeView is in the products app

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
