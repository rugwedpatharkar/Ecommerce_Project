"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.http import HttpResponse

urlpatterns = [
    path('', include('ecommerce_project_home.urls')),
    path('accounts/', include('ecommerce_project_accounts.urls')),
    path('products/', include('ecommerce_project_products.urls')),
    path('admin/', admin.site.urls),
    path('favicon.ico', lambda x: HttpResponse(status=204)),
    path('transactions/', include('ecommerce_project_transactions.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
admin.site.cookie_name = 'admin_sessionid'  # Update with your admin session name
