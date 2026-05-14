"""
Настройка административной панели Django
Соответствует п.1.2.2 диплома - простая встроенная админ-панель
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, CartItem, Order, OrderItem, WishlistItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ['name', 'slug', 'gender', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['gender']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Кол-во товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения товаров в админке"""
    list_display = [
        'id', 'name', 'category', 'gender', 'display_price',
        'available', 'is_new', 'is_sale', 'views_count', 'created_at'
    ]
    list_filter = [
        'category', 'gender', 'available', 'is_new', 'is_sale',
        'subcategory', 'collection', 'season'
    ]
    list_editable = ['available', 'is_new', 'is_sale']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description', 'gender')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'sale_price', 'is_sale', 'available', 'is_new')
        }),
        ('Классификация', {
            'fields': ('subcategory', 'collection', 'season')
        }),
        ('Характеристики', {
            'fields': ('size', 'color', 'material')
        }),
        ('Изображения', {
            'fields': ('image_url', 'image', 'image_preview', 'image_2', 'image_3')
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_price(self, obj):
        if obj.is_sale and obj.sale_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">{}₽</span> '
                '<span style="color: #e74c3c; font-weight: bold;">{}₽</span>',
                obj.price, obj.sale_price
            )
        return f"{obj.price}₽"
    display_price.short_description = 'Цена'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Предпросмотр'


class OrderItemInline(admin.TabularInline):
    """Встроенный класс для отображения позиций заказа"""
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product', 'product_name', 'size', 'price', 'quantity', 'total_price_display']
    fields = ['product', 'product_name', 'size', 'price', 'quantity', 'total_price_display']
    
    def total_price_display(self, obj):
        if obj.pk:
            return f"{obj.price * obj.quantity}₽"
        return "-"
    total_price_display.short_description = 'Сумма'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройка отображения заказов в админке"""
    list_display = [
        'id', 'get_full_name', 'phone', 'total_price',
        'status', 'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Детали заказа', {
            'fields': ('status', 'payment_method', 'total_price', 'comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Настройка отображения корзины в админке"""
    list_display = ['id', 'product', 'quantity', 'size_selected', 'user', 'added_at']
    list_filter = ['added_at']
    search_fields = ['product__name', 'user__username']


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    """Настройка отображения избранного в админке"""
    list_display = ['id', 'product', 'user', 'added_at']
    search_fields = ['product__name', 'user__username']