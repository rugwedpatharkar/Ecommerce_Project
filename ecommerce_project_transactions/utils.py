# transactions/utils.py
from .models import CartItem
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def calculate_cart_total(cart_items):
    total_amount = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    
    for cart_item in cart_items:
        print(f"Item: {cart_item.product.title}, Price: {cart_item.product.price}, Quantity: {cart_item.quantity}")

    print("Total amount calculated:", total_amount)  # Debugging line
    return total_amount



def generate_invoice_pdf(order):
    template_path = 'transactions/invoice_template.html'
    context = {'order': order}
    
    # Create a Django response object with appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'

    # Render the template to a buffer
    template = get_template(template_path)
    html = template.render(context)

    # Create the PDF object, and write it to the response
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
