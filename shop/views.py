"""
Представления (контроллеры) для интернет-магазина SeeYouInside
Обработка запросов: каталог, корзина, избранное, оформление заказа
Соответствует п.2.1.2 и п.2.2 дипломного проекта
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.text import slugify
from decimal import Decimal

from .models import Category, Product, CartItem, Order, OrderItem, WishlistItem
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


def index(request):
    """Главная страница магазина"""
    new_products = Product.objects.filter(available=True, is_new=True).order_by('-created_at')[:8]
    popular_products = Product.objects.filter(available=True).order_by('-views_count')[:4]
    sale_products = Product.objects.filter(available=True, is_sale=True).order_by('-created_at')[:4]
    categories = Category.objects.annotate(product_count=Count('products', filter=Q(products__available=True)))
    
    context = {
        'new_products': new_products,
        'popular_products': popular_products,
        'sale_products': sale_products,
        'categories': categories,
        'page_title': 'SeeYouInside - Магазин стильной одежды',
    }
    return render(request, 'shop/index.html', context)


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next', 'shop:profile')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form, 'page_title': 'Вход | SeeYouInside'})


def logout_view(request):
    """Выход"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('shop:index')


def register_view(request):
    """Регистрация"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
                return render(request, 'shop/register.html', {'form': form, 'page_title': 'Регистрация | SeeYouInside'})
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('shop:profile')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form, 'page_title': 'Регистрация | SeeYouInside'})


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()
        request.session['user_phone'] = request.POST.get('phone', '').strip()
        request.session['user_address'] = request.POST.get('address', '').strip()
        messages.success(request, 'Данные обновлены!')
        return redirect('shop:profile')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    phone = request.session.get('user_phone', '')
    address = request.session.get('user_address', '')
    
    context = {
        'user': request.user,
        'phone': phone,
        'address': address,
        'orders': orders,
        'page_title': 'Личный кабинет | SeeYouInside'
    }
    return render(request, 'shop/profile.html', context)


def catalog(request, category_slug=None):
    """Страница каталога с полной фильтрацией"""
    category = None
    categories = Category.objects.annotate(product_count=Count('products', filter=Q(products__available=True)))
    products = Product.objects.filter(available=True).select_related('category')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(color__icontains=query))
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try: products = products.filter(price__gte=Decimal(min_price))
        except: pass
    if max_price:
        try: products = products.filter(price__lte=Decimal(max_price))
        except: pass
    
    size_filter = request.GET.get('size')
    if size_filter: products = products.filter(size__icontains=size_filter)
    color_filter = request.GET.get('color')
    if color_filter: products = products.filter(color__icontains=color_filter)
    
    new_only = request.GET.get('new_only')
    if new_only: products = products.filter(is_new=True)
    sale_only = request.GET.get('sale_only')
    if sale_only: products = products.filter(is_sale=True)
    
    gender = request.GET.get('gender')
    if gender: products = products.filter(gender=gender)
    subcategory = request.GET.get('subcategory')
    if subcategory: products = products.filter(subcategory=subcategory)
    collection = request.GET.get('collection')
    if collection: products = products.filter(collection=collection)
    season = request.GET.get('season')
    if season: products = products.filter(season=season)
    
    sort_by = request.GET.get('sort', '-created_at')
    sort_options = {
        '-created_at': 'Новинки', 'created_at': 'Сначала старые',
        'price': 'Цена ↑', '-price': 'Цена ↓',
        'name': 'А-Я', '-name': 'Я-А', '-views_count': 'Популярные',
    }
    products = products.order_by(sort_by) if sort_by in sort_options else products.order_by('-created_at')
    
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try: products_page = paginator.page(page)
    except PageNotAnInteger: products_page = paginator.page(1)
    except EmptyPage: products_page = paginator.page(paginator.num_pages)
    
    all_products_for_filters = Product.objects.filter(available=True)
    if category: all_products_for_filters = all_products_for_filters.filter(category=category)
    all_sizes = set(); all_colors = set()
    for p in all_products_for_filters:
        if p.size: all_sizes.update([s.strip() for s in p.size.split(',') if s.strip()])
        if p.color: all_colors.add(p.color.strip())
    
    total_products = products.count()
    page_title = f'{category.name} | Каталог' if category else 'Каталог одежды | SeeYouInside'
    
    context = {
        'category': category, 'categories': categories, 'products': products_page,
        'total_products': total_products, 'query': query,
        'min_price': min_price, 'max_price': max_price,
        'size_filter': size_filter, 'color_filter': color_filter,
        'new_only': new_only, 'sale_only': sale_only,
        'gender': gender, 'subcategory': subcategory,
        'collection': collection, 'season': season,
        'all_sizes': sorted(all_sizes), 'all_colors': sorted(all_colors),
        'sort_by': sort_by, 'sort_options': sort_options,
        'page_title': page_title,
    }
    return render(request, 'shop/catalog.html', context)


def product_detail(request, id, slug):
    """Карточка товара"""
    product = get_object_or_404(Product.objects.select_related('category'), id=id, slug=slug, available=True)
    product.views_count += 1
    product.save(update_fields=['views_count'])
    
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id).order_by('-views_count')[:4]
    sizes = product.get_sizes_list()
    
    in_cart = False
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
    
    specifications = []
    if product.material: specifications.append({'name': 'Состав', 'value': product.material})
    if product.color: specifications.append({'name': 'Цвет', 'value': product.color})
    specifications.append({'name': 'Категория', 'value': product.category.name})
    if product.size: specifications.append({'name': 'Размеры', 'value': product.size})
    
    context = {
        'product': product, 'sizes': sizes,
        'related_products': related_products,
        'in_wishlist': in_wishlist, 'specifications': specifications,
        'page_title': f'{product.name} | SeeYouInside',
    }
    return render(request, 'shop/detail.html', context)


# ============================================================
# ЛОГИКА КОРЗИНЫ
# ============================================================

def get_cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
        request.session['cart_id'] = cart_id
    return cart_id


def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).select_related('product', 'product__category')
    return CartItem.objects.filter(session_key=get_cart_id(request)).select_related('product', 'product__category')


def get_cart_count(request):
    return sum(item.quantity for item in get_cart_items(request))


def get_cart_total(request):
    return sum(item.total_price() for item in get_cart_items(request))


@require_POST
def cart_add(request, product_id):
    """Добавление товара в корзину (обычная отправка)"""
    product = get_object_or_404(Product, id=product_id)
    if not product.available:
        messages.error(request, 'Товар недоступен')
        return redirect('shop:product_detail', id=product.id, slug=product.slug)
    
    size = request.POST.get('size', '').strip()
    quantity = min(max(int(request.POST.get('quantity', 1)), 1), 10)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, 
            product=product, 
            size_selected=size or None, 
            defaults={'quantity': quantity}
        )
    else:
        cart_item, created = CartItem.objects.get_or_create(
            session_key=get_cart_id(request), 
            product=product, 
            size_selected=size or None, 
            defaults={'quantity': quantity}
        )
    
    if not created:
        cart_item.quantity = min(cart_item.quantity + quantity, 10)
        cart_item.save()
    
    messages.success(request, f'✅ "{product.name}" добавлен в корзину')
    return redirect('shop:product_detail', id=product.id, slug=product.slug)


@require_POST
def cart_add_ajax(request, product_id):
    """Добавление товара в корзину через AJAX (возвращает JSON)"""
    product = get_object_or_404(Product, id=product_id, available=True)
    
    size = request.POST.get('size', '').strip()
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, 10))
    
    # Поиск существующего товара в корзине
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size_selected=size if size else None,
            defaults={'quantity': quantity}
        )
    else:
        cart_id = get_cart_id(request)
        cart_item, created = CartItem.objects.get_or_create(
            session_key=cart_id,
            product=product,
            size_selected=size if size else None,
            defaults={'quantity': quantity}
        )
    
    if not created:
        cart_item.quantity = min(cart_item.quantity + quantity, 10)
        cart_item.save()
    
    return JsonResponse({
        'success': True,
        'message': f'{product.name} добавлен в корзину',
        'cart_count': get_cart_count(request),
        'cart_total': str(get_cart_total(request))
    })


def cart_detail(request):
    cart_items = get_cart_items(request)
    cart_total = sum(item.total_price() for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)
    request.session['cart_count'] = cart_count
    
    recommended_products = []
    if cart_items:
        cats = set(item.product.category_id for item in cart_items)
        recommended_products = Product.objects.filter(category_id__in=cats, available=True).exclude(id__in=[item.product_id for item in cart_items]).order_by('-views_count')[:4]
    
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'cart_total': cart_total, 'cart_count': cart_count, 'recommended_products': recommended_products, 'page_title': 'Корзина | SeeYouInside'})


@require_POST
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')
    if action == 'increase' and cart_item.quantity < 10:
        cart_item.quantity += 1; cart_item.save()
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0: cart_item.delete()
        else: cart_item.save()
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, item_id):
    get_object_or_404(CartItem, id=item_id).delete()
    messages.success(request, 'Товар удалён из корзины')
    return redirect('shop:cart_detail')


def cart_clear(request):
    get_cart_items(request).delete()
    messages.success(request, 'Корзина очищена')
    return redirect('shop:cart_detail')


# ============================================================
# ЛОГИКА ИЗБРАННОГО
# ============================================================

def wishlist_toggle(request, product_id):
    """Добавление/удаление из избранного"""
    if not request.user.is_authenticated:
        messages.warning(request, '🔒 Чтобы добавить товар в избранное, войдите или зарегистрируйтесь в программе лояльности SeeYouInside CLUB')
        return redirect('shop:login')
    
    product = get_object_or_404(Product, id=product_id, available=True)
    wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f'💔 "{product.name}" удалён из избранного')
    else:
        WishlistItem.objects.create(user=request.user, product=product)
        messages.success(request, f'❤️ "{product.name}" добавлен в избранное')
    
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


def wishlist_detail(request):
    """Страница избранного"""
    if not request.user.is_authenticated:
        messages.warning(request, '🔒 Войдите или зарегистрируйтесь, чтобы просмотреть избранное')
        return redirect('shop:login')
    
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
        'page_title': 'Избранное | SeeYouInside',
    }
    return render(request, 'shop/wishlist.html', context)


def get_wishlist_count(request):
    """Возвращает количество товаров в избранном"""
    if request.user.is_authenticated:
        return WishlistItem.objects.filter(user=request.user).count()
    return 0


# ============================================================
# ЗАКАЗЫ
# ============================================================

def checkout(request):
    """Страница оформления заказа"""
    if not request.user.is_authenticated:
        messages.warning(request, '🔒 Чтобы оформить заказ, войдите или зарегистрируйтесь в программе лояльности SeeYouInside CLUB')
        return redirect('shop:login')
    
    cart_items = get_cart_items(request)
    if not cart_items.exists():
        messages.warning(request, 'Корзина пуста')
        return redirect('shop:catalog')
    
    cart_total = sum(item.total_price() for item in cart_items)
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_price=cart_total
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, product_name=item.product.name, size=item.size_selected, price=item.product.get_current_price(), quantity=item.quantity)
        cart_items.delete()
        request.session['cart_count'] = 0
        messages.success(request, f'🎉 Заказ №{order.id} оформлен!')
        return redirect('shop:order_success', order_id=order.id)
    
    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total, 'page_title': 'Оформление заказа | SeeYouInside'})


def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id)
    return render(request, 'shop/success.html', {'order': order, 'page_title': f'Заказ №{order.id} | SeeYouInside'})


# ============================================================
# ИНФО-СТРАНИЦЫ
# ============================================================

def about(request): return render(request, 'shop/about.html', {'page_title': 'О магазине | SeeYouInside'})
def contacts(request): return render(request, 'shop/contacts.html', {'page_title': 'Контакты | SeeYouInside'})
def delivery(request): return render(request, 'shop/delivery.html', {'page_title': 'Доставка | SeeYouInside'})


# ============================================================
# AJAX
# ============================================================

@require_POST
def quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    html = f'<div class="quick-view"><div class="row"><div class="col-md-6"><img src="/static/products/{product.slug}.jpg" class="img-fluid" alt="{product.name}"></div><div class="col-md-6"><h4>{product.name}</h4><p class="price">{product.get_current_price()} ₽</p><p class="description">{product.description[:200]}...</p><a href="{product.get_absolute_url()}" class="btn btn-dark w-100">Подробнее</a></div></div></div>'
    return JsonResponse({'success': True, 'html': html})


def get_header_info(request):
    """Возвращает информацию о корзине и избранном в JSON"""
    return JsonResponse({
        'cart_count': get_cart_count(request),
        'cart_total': str(get_cart_total(request)),
        'wishlist_count': get_wishlist_count(request),
    })


def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    if len(query) >= 2:
        for p in Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), available=True).values('id', 'name', 'price', 'slug')[:5]:
            suggestions.append({'id': p['id'], 'name': p['name'], 'price': str(p['price']), 'url': reverse('shop:product_detail', args=[p['id'], p['slug']])})
    return JsonResponse({'suggestions': suggestions})


# ============================================================
# ОБРАБОТЧИКИ ОШИБОК
# ============================================================

def page_not_found(request, exception=None):
    return render(request, 'shop/404.html', {'page_title': '404 | SeeYouInside'}, status=404)

def server_error(request):
    return render(request, 'shop/500.html', {'page_title': '500 | SeeYouInside'}, status=500)

def permission_denied(request, exception=None):
    return render(request, 'shop/403.html', {'page_title': '403 | SeeYouInside'}, status=403)