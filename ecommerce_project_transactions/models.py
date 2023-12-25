from django.db import models
from ecommerce_project_products.models import Product
from ecommerce_project_accounts.models import Profile, Address

class Card(models.Model):
    cardtype = models.CharField(max_length=50)
    name_on_card = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    exp_month = models.PositiveIntegerField()
    exp_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cardtype} - {self.name_on_card}"

class UpiID(models.Model):
    paymentApp = models.CharField(max_length=50)
    upiId = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.paymentApp} - {self.upiId}"

class PaymentOptions(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payment_options')
    cards = models.ManyToManyField(Card, blank=True)
    upiIDs = models.ManyToManyField(UpiID, blank=True)

    def __str__(self):
        return f"Payment Options for {self.profile.user.username}"

class LikedItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='liked_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='liked_by')

    def __str__(self):
        return f"{self.profile.user.username} likes {self.product.title}"

class CartItemManager(models.Manager):
    def get_non_removed_items(self, profile):
        return self.filter(profile=profile, is_removed=False)

class CartItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_cart')
    quantity = models.PositiveIntegerField(default=1)
    is_removed = models.BooleanField(default=False)
    objects = CartItemManager()

class OrderedItem(models.Model):
    STATUS_CHOICES = [
        ('shipped', 'Shipped'),
        ('dispatched', 'Dispatched'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('pending', 'Pending')
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('cash_on_delivery', 'Cash on Delivery')
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ordered_items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_in')
    quantity = models.PositiveIntegerField()
    item_total = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='shipped')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='cash_on_delivery')
    unit_price = models.FloatField(null=True)
    total_price = models.FloatField(null=True)
    cart_item = models.ForeignKey(CartItem, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not isinstance(self.quantity, int):
            self.quantity = int(self.quantity)
        if not isinstance(self.unit_price, float):
            self.unit_price = float(self.unit_price)

        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} - Status: {self.get_status_display()}"
