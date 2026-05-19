from .views import get_cart_count, get_cart_total, get_wishlist_count

def cart_context(request):
    """Добавляет данные о корзине и избранном во все шаблоны"""
    return {
        'cart_count': get_cart_count(request),
        'cart_total': get_cart_total(request),
        'wishlist_count': get_wishlist_count(request),
    }