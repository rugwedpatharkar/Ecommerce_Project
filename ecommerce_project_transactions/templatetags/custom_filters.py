# transactions/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg


@register.filter(name='total_cart_amount')
def total_cart_amount(cart_items):
    # Your logic to calculate the total amount goes here
    return sum(item.product.price * item.quantity for item in cart_items)