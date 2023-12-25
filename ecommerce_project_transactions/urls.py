from django.urls import path
from .views import (
    add_to_liked_items,
    remove_from_liked_items,
    show_liked_items,
    add_to_cart,
    RemoveFromCartView,
    view_cart,
    place_order,
    download_invoice,
    view_orders
)
from . import views


app_name = 'transactions'

urlpatterns = [
    path('add-to-liked-items/<slug:product_slug>/', views.add_to_liked_items, name='add_to_liked_items'),
    path('remove-from-liked-items/<str:product_slug>/', remove_from_liked_items, name='remove_from_liked_items'),
    path('show-liked-items/', show_liked_items, name='show_liked_items'),
    path('add-to-cart/<slug:product_slug>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('payment-options/', views.view_payment_options, name='view_payment_options'),
    path('add-card/', views.add_card, name='add_card'),
    path('add-upi-id/', views.add_upi_id, name='add_upi_id'),
    path('update-card/<int:card_id>/', views.update_card, name='update_card'),
    path('delete-card/<int:card_id>/', views.delete_card, name='delete_card'),
    path('update-upi-id/<int:upi_id>/', views.update_upi_id, name='update_upi_id'),
    path('delete-upi-id/<int:upi_id>/', views.delete_upi_id, name='delete_upi_id'),
    path('order-items/', views.order_items, name='order_items'),
    path('place-order/', views.place_order, name='place_order'),
    path('view-orders/', views.view_orders, name='view_orders'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('place_order/', place_order, name='place_order'),
    path('view_orders/', view_orders, name='view_orders'),
    path('download-invoice/<int:order_id>/', download_invoice, name='download_invoice'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),



]
