from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Card, UpiID, PaymentOptions, LikedItem, CartItem, OrderedItem

class CardResource(resources.ModelResource):
    class Meta:
        model = Card

if admin.site.is_registered(Card):
    admin.site.unregister(Card)
    
@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    resource_class = CardResource
    list_display = ('cardtype', 'name_on_card', 'card_number', 'exp_month', 'exp_year')
    search_fields = ('cardtype', 'name_on_card', 'card_number')
    ordering = ('cardtype', 'name_on_card', 'card_number')



if admin.site.is_registered(UpiID):
    admin.site.unregister(UpiID)

class UpiIDResource(resources.ModelResource):
    class Meta:
        model = UpiID

@admin.register(UpiID)
class UpiIDAdmin(ImportExportModelAdmin):
    resource_class = UpiIDResource
    list_display = ('paymentApp', 'upiId')
    search_fields = ('paymentApp', 'upiId')
    ordering = ('paymentApp', 'upiId')


if admin.site.is_registered(PaymentOptions):
    admin.site.unregister(PaymentOptions)

class PaymentOptionsResource(resources.ModelResource):
    class Meta:
        model = PaymentOptions

@admin.register(PaymentOptions)
class PaymentOptionsAdmin(ImportExportModelAdmin):
    resource_class = PaymentOptionsResource
    list_display = ('profile', 'get_cards', 'get_upi_ids')
    search_fields = ('profile__user__username',)
    ordering = ('profile__user__username',)

    def get_cards(self, obj):
        return ", ".join([card.name_on_card for card in obj.cards.all()])

    get_cards.short_description = 'Cards'

    def get_upi_ids(self, obj):
        return ", ".join([upi.upiId for upi in obj.upiIDs.all()])

    get_upi_ids.short_description = 'UPI IDs'


if admin.site.is_registered(LikedItem):
    admin.site.unregister(LikedItem)

class LikedItemResource(resources.ModelResource):
    class Meta:
        model = LikedItem

@admin.register(LikedItem)
class LikedItemAdmin(ImportExportModelAdmin):
    resource_class = LikedItemResource
    list_display = ('profile', 'product')
    search_fields = ('profile__user__username', 'product__title')
    ordering = ('profile__user__username', 'product__title')


if admin.site.is_registered(CartItem):
    admin.site.unregister(CartItem)


class CartItemResource(resources.ModelResource):
    class Meta:
        model = CartItem

@admin.register(CartItem)
class CartItemAdmin(ImportExportModelAdmin):
    resource_class = CartItemResource
    list_display = ('profile', 'product', 'quantity', 'is_removed')
    search_fields = ('profile__user__username', 'product__title')
    list_filter = ('is_removed',)
    ordering = ('profile__user__username', 'product__title')



if admin.site.is_registered(OrderedItem):
    admin.site.unregister(OrderedItem)

class OrderedItemResource(resources.ModelResource):
    class Meta:
        model = OrderedItem

@admin.register(OrderedItem)
class OrderedItemAdmin(ImportExportModelAdmin):
    resource_class = OrderedItemResource
    list_display = ('profile', 'product', 'quantity', 'item_total', 'address', 'status', 'payment_status')
    search_fields = ('profile__user__username', 'product__title', 'address__city', 'status', 'payment_status')
    list_filter = ('status', 'payment_status')
    ordering = ('profile__user__username', 'product__title', 'status', 'payment_status')

