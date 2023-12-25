from .models import LikedItem, CartItem, OrderedItem


def liked_cart_count(request):
    liked_items_count = 0
    cart_items_count = 0
    ordered_items_count = 0
    
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        liked_items_count = LikedItem.objects.filter(profile=request.user.profile).count()
        cart_items_count = CartItem.objects.filter(profile=request.user.profile).count()
        ordered_items_count= OrderedItem.objects.filter(profile=request.user.profile).count()
    return {
        'liked_items_count': liked_items_count,
        'cart_items_count': cart_items_count,
        'ordered_items_count': ordered_items_count,

    }
