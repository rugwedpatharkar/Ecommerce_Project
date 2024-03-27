import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import LikedItem, CartItem, PaymentOptions, Card, UpiID, OrderedItem, Address
from ecommerce_project_products.models import Product
from ecommerce_project_accounts.models import Address
from django.contrib import messages
from django.views import View
from django.db import transaction
from .utils import calculate_cart_total
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
import razorpay



@login_required
def add_to_liked_items(request, product_slug):
    profile = request.user.profile
    product = get_object_or_404(Product, slug=product_slug)
    
    if not LikedItem.objects.filter(profile=profile, product=product).exists():
        liked_item = LikedItem(profile=profile, product=product)
        liked_item.save()
        messages.success(request, f"{product.title} added to your liked item list.")
    
    return redirect('transactions:show_liked_items')


@login_required
def show_liked_items(request):
    profile = request.user.profile
    paginate_by = 10
    liked_items = LikedItem.objects.filter(profile=profile)
    context = {'liked_items': liked_items}
    return render(request, 'transactions/likedItems.html', context)


@login_required
def remove_from_liked_items(request, product_slug):
    profile = request.user.profile
    product = get_object_or_404(Product, slug=product_slug)
    
    try:
        liked_item = LikedItem.objects.get(profile=profile, product=product)
        liked_item.delete()
        messages.success(request, f"{product.title} removed from liked items successfully.")
    except LikedItem.DoesNotExist:
        messages.warning(request, f'{product.title} is not in your liked items.')
    
    return redirect('transactions:show_liked_items')


def view_cart(request):
    cart_items = CartItem.objects.filter(profile=request.user.profile, is_removed=False)
    total_amount = calculate_cart_total(cart_items)
    user_payment_options = PaymentOptions.objects.filter(profile=request.user.profile).first()
    cards = Card.objects.filter(paymentoptions__profile=request.user.profile)
    upi_ids = UpiID.objects.filter(paymentoptions__profile=request.user.profile)
    shipping_addresses = Address.objects.filter(profile=request.user.profile)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'payment_options': user_payment_options,
        'cards': cards,
        'upi_ids': upi_ids,
        'shipping_addresses': shipping_addresses,
    }
    return render(request, 'transactions/view_cart.html', context)

class RemoveFromCartView(View):
    def get(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, profile=request.user.profile)
        cart_item.delete()
        messages.success(request, 'Product removed from the cart successfully.')
        return redirect('transactions:view_cart')


@login_required
def add_to_cart(request, product_slug):
    profile = request.user.profile
    product = get_object_or_404(Product, slug=product_slug)
    existing_item = CartItem.objects.filter(profile=profile, product=product).first()
    
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
        messages.success(request, f"{product.title} added to your cart. Quantity updated.")
    else:
        cart_item = CartItem(profile=profile, product=product)
        cart_item.save()
        messages.success(request, f"{product.title} added to your cart.")
    
    return redirect('transactions:view_cart')


def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Quantity of {cart_item.product.title} increased.")
    return redirect('transactions:view_cart')


def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.title} decreased.")
    else:
        cart_item.delete()
        messages.success(request, f"{cart_item.product.title} removed from your cart.")
    
    return redirect('transactions:view_cart')


def add_card(request):
    if request.method == 'POST':
        cardtype = request.POST.get('cardtype')
        name_on_card = request.POST.get('name_on_card')
        card_number = request.POST.get('card_number')
        exp_month = request.POST.get('exp_month')
        exp_year = request.POST.get('exp_year')
        card = Card.objects.create(cardtype=cardtype, name_on_card=name_on_card, card_number=card_number, exp_month=exp_month, exp_year=exp_year)
        payment_options = get_or_create_payment_options(request.user.profile)
        payment_options.cards.add(card)
        messages.success(request, 'Card added successfully.')
        return redirect('transactions:view_payment_options')
    
    return render(request, 'transactions/add_card.html')


def add_upi_id(request):
    if request.method == 'POST':
        paymentApp = request.POST.get('paymentApp')
        upiId = request.POST.get('upiId')
        upi_id = UpiID.objects.create(paymentApp=paymentApp, upiId=upiId)
        payment_options = get_or_create_payment_options(request.user.profile)
        payment_options.upiIDs.add(upi_id)
        messages.success(request, 'UPI ID added successfully.')
        return redirect('transactions:view_payment_options')
    
    return render(request, 'transactions/add_upi_id.html')


def update_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    
    if request.method == 'POST':
        card.cardtype = request.POST.get('cardtype')
        card.name_on_card = request.POST.get('name_on_card')
        card.card_number = request.POST.get('card_number')
        card.exp_month = request.POST.get('exp_month')
        card.exp_year = request.POST.get('exp_year')
        card.save()
        return redirect('transactions:view_payment_options')
    
    return render(request, 'transactions/update_card.html', {'card': card})


def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    return redirect('transactions:view_payment_options')


def update_upi_id(request, upi_id):
    upi_id_obj = get_object_or_404(UpiID, id=upi_id)
    if request.method == 'POST':
        upi_id_obj.paymentApp = request.POST.get('paymentApp')
        upi_id_obj.upiId = request.POST.get('upiId')
        upi_id_obj.save()
        return redirect('transactions:view_payment_options')
    return render(request, 'transactions/update_upi_id.html', {'upi_id': upi_id_obj})


def delete_upi_id(request, upi_id):
    upi_id_obj = get_object_or_404(UpiID, id=upi_id)
    upi_id_obj.delete()
    return redirect('transactions:view_payment_options')


def get_or_create_payment_options(profile):
    payment_options, created = PaymentOptions.objects.get_or_create(profile=profile)
    return payment_options


def view_payment_options(request):
    user_payment_options = PaymentOptions.objects.filter(profile=request.user.profile).first()
    cards = Card.objects.filter(paymentoptions__profile=request.user.profile)
    upi_ids = UpiID.objects.filter(paymentoptions__profile=request.user.profile)
    
    context = {
        'payment_options': user_payment_options,
        'cards': cards,
        'upi_ids': upi_ids,
    }
    return render(request, 'transactions/payment_options.html', context)


@login_required
def order_items(request):
    cart_items = CartItem.objects.filter(profile=request.user.profile)
    total_amount = calculate_cart_total(cart_items)
    user_payment_options = PaymentOptions.objects.filter(profile=request.user.profile).first()
    cards = Card.objects.filter(paymentoptions__profile=request.user.profile)
    upi_ids = UpiID.objects.filter(paymentoptions__profile=request.user.profile)
    shipping_addresses = Address.objects.filter(profile=request.user.profile)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'payment_options': user_payment_options,
        'cards': cards,
        'upi_ids': upi_ids,
        'shipping_addresses': shipping_addresses,
    }
    return render(request, 'transactions/order_items.html', context)



def place_order(request):
    if request.method == 'POST':
        cart_item_ids = request.POST.getlist('cart_item_id')
        quantities = request.POST.getlist('quantity')
        selected_payment_option = request.POST.get('payment_option')
        selected_shipping_address_id = request.POST.get('shipping_address')
        selected_shipping_address_id = int(selected_shipping_address_id) if selected_shipping_address_id else None
        total_amount = 0
        cart_items = CartItem.objects.get_non_removed_items(request.user.profile)

        if not cart_items:
            messages.warning(request, 'Your cart is empty. Please add items to your cart before placing an order.')
            return redirect('transactions:view_cart')

        selected_shipping_address = get_object_or_404(Address, id=selected_shipping_address_id)
        temp_cart_items = []

        for cart_item_id, quantity in zip(cart_item_ids, quantities):
            cart_item = get_object_or_404(CartItem, id=cart_item_id, profile=request.user.profile)
            total_amount += cart_item.product.price * int(quantity)

            if cart_item.product.stock < int(quantity):
                messages.error(request, f'Not enough stock available for {cart_item.product.title}. Please update your quantity.')
                return redirect('transactions:view_cart')

            cart_item.product.stock -= int(quantity)
            cart_item.product.save()

            temp_cart_items.append({
                'id': cart_item.id,
                'title': cart_item.product.title,
                'image': cart_item.product.image.url,
                'quantity': int(quantity),
                'total_price': cart_item.product.price * int(quantity),
            })

        if selected_payment_option == 'paid':
            request.session['temp_cart_items'] = temp_cart_items
            request.session['selected_payment_option'] = selected_payment_option

            user = request.user
            user_email = user.email
            user_name = user.get_full_name()
            user_contact = user.profile.contact_number
            amount = int(total_amount * 100)
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            payment_data = {
                "amount": amount,
                "currency": "INR",
                "receipt": "order_receipt",
                "notes": {
                    "email": user_email,
                },
            }
            order = client.order.create(data=payment_data)
            request.session['order_id'] = order['id']
            request.session['total_amount'] = total_amount
            request.session['selected_shipping_address'] = selected_shipping_address_id

            return render(request, 'transactions/payment.html', {
                'order_id': order['id'],
                'amount': total_amount,
                'currency': "INR",
                'key': settings.RAZORPAY_API_KEY,
                'name': 'GadgetGalaxy',
                'description': 'Payment for Your Product',
                'image': '/media/img/favicon.ico',
                'email': user_email,
                'name': user_name,
                'contact': user_contact,
                'temp_cart_items': temp_cart_items,
            })
        else:
            for cart_item_data in temp_cart_items:
                cart_item_id = cart_item_data['id']
                quantity = cart_item_data['quantity']
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                OrderedItem.objects.create(
                    profile=request.user.profile,
                    product=cart_item.product,
                    quantity=quantity,
                    item_total=cart_item.product.price * int(quantity),
                    address=selected_shipping_address,
                    status='pending',
                    payment_status=selected_payment_option,
                    unit_price=cart_item.product.price,
                    total_price=cart_item.product.price * int(quantity),
                    cart_item=cart_item,
                )
                cart_item.delete()

            messages.success(request, f'Order placed successfully! Total Amount: ₹{total_amount}')
            return redirect('transactions:view_orders')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('transactions:view_cart')

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        selected_shipping_address_id = request.session.get('selected_shipping_address')
        selected_payment_option = request.session.get('selected_payment_option')

        if selected_shipping_address_id is None or selected_payment_option is None:
            return HttpResponseBadRequest("Missing session data")

        selected_shipping_address = get_object_or_404(Address, id=selected_shipping_address_id)

        temp_cart_items = request.session.pop('temp_cart_items', None)
        if not temp_cart_items:
            return HttpResponseBadRequest("Missing 'temp_cart_items' data")

        for cart_item_data in temp_cart_items:
            cart_item_id = cart_item_data['id']
            quantity = cart_item_data['quantity']
            cart_item = get_object_or_404(CartItem, id=cart_item_id, profile=request.user.profile)
            OrderedItem.objects.create(
                profile=request.user.profile,
                product=cart_item.product,
                quantity=int(quantity),
                item_total=cart_item.product.price * int(quantity),
                address=selected_shipping_address,
                status='pending',
                payment_status=selected_payment_option,
                unit_price=cart_item.product.price,
                total_price=cart_item.product.price * int(quantity),
                cart_item=cart_item,
            )
            cart_item.delete()

        del request.session['selected_payment_option']
        del request.session['selected_shipping_address']

        messages.success(request, f'Order placed successfully.')
        return redirect('transactions:view_orders')
    else:
        return HttpResponseBadRequest("Invalid request method")



def view_orders(request):
    orders = OrderedItem.objects.filter(profile=request.user.profile)
    context = {'orders': orders}
    return render(request, 'transactions/view_orders.html', context)

    
def view_orders(request):
    orders = OrderedItem.objects.filter(profile=request.user.profile)
    context = {'orders': orders}
    return render(request, 'transactions/view_orders.html', context)


def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="invoice.pdf"'

    encoding = 'utf-8'
    html = html.encode(encoding)

    pisa_status = pisa.CreatePDF(html, dest=response, encoding=encoding)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def download_invoice(request, order_id):
    order = get_object_or_404(OrderedItem, id=order_id)
    if order.status != 'delivered':
        return HttpResponse("Invoice is only available for delivered orders.")
    context = {
        'order': order,
    }
    pdf = render_to_pdf('transactions/invoice_template.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"invoice_{order.id}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF")


