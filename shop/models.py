"""
Модели базы данных для интернет-магазина SeeYouInside
Содержит категории, товары, корзину, избранное и заказы
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Модель категорий товаров"""
    GENDER_CHOICES = (
        ('women', 'Женское'),
        ('men', 'Мужское'),
        ('unisex', 'Унисекс'),
    )
    
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категории")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', verbose_name="Пол")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:catalog_category', args=[self.slug])


class Product(models.Model):
    """Модель товара"""
    GENDER_CHOICES = (
        ('women', 'Женское'),
        ('men', 'Мужское'),
        ('unisex', 'Унисекс'),
    )
    
    SUBCATEGORY_CHOICES = (
        ('dresses', 'Платья'),
        ('blouses', 'Блузы и рубашки'),
        ('jeans_women', 'Джинсы'),
        ('trousers_women', 'Брюки'),
        ('skirts', 'Юбки'),
        ('jackets_women', 'Жакеты и пиджаки'),
        ('knitwear', 'Трикотаж'),
        ('outerwear_women', 'Верхняя одежда'),
        ('shirts', 'Рубашки'),
        ('tshirts', 'Футболки'),
        ('jeans_men', 'Джинсы'),
        ('trousers_men', 'Брюки'),
        ('hoodies', 'Худи и свитшоты'),
        ('jackets_men', 'Куртки'),
        ('suits', 'Костюмы'),
        ('outerwear_men', 'Верхняя одежда'),
        ('bags', 'Сумки'),
        ('belts', 'Ремни'),
        ('hats', 'Головные уборы'),
        ('scarves', 'Шарфы и платки'),
        ('gloves', 'Перчатки'),
        ('jewelry', 'Украшения'),
        ('glasses', 'Очки'),
        ('sneakers', 'Кроссовки'),
        ('heels', 'Туфли'),
        ('boots', 'Ботинки'),
        ('winter_boots', 'Сапоги'),
        ('flats', 'Балетки'),
        ('loafers', 'Лоферы'),
        ('sandals', 'Сандалии'),
    )
    
    COLLECTION_CHOICES = (
        ('basic', 'Базовая коллекция'),
        ('evening', 'Вечерняя коллекция'),
        ('sport', 'Спортивная коллекция'),
        ('business', 'Деловая коллекция'),
        ('casual', 'Повседневная коллекция'),
        ('city', 'Капсула "Город"'),
        ('relax', 'Капсула "Отдых"'),
        ('limited', 'Limited Edition'),
    )
    
    SEASON_CHOICES = (
        ('spring-summer-2026', 'Весна-Лето 2026'),
        ('autumn-winter-2026', 'Осень-Зима 2026'),
        ('cruise', 'Круизная коллекция'),
        ('preorder', 'Предзаказ'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, verbose_name="URL-идентификатор")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', verbose_name="Пол")
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True, verbose_name="Подкатегория")
    collection = models.CharField(max_length=50, choices=COLLECTION_CHOICES, blank=True, null=True, verbose_name="Коллекция")
    season = models.CharField(max_length=50, choices=SEASON_CHOICES, blank=True, null=True, verbose_name="Сезон")
    
    size = models.CharField(max_length=100, blank=True, null=True, verbose_name="Доступные размеры")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Цвет")
    material = models.CharField(max_length=200, blank=True, null=True, verbose_name="Состав/материал")
    
    # Загружаемые фото (оставляем, но НЕ ИСПОЛЬЗУЕМ)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Главное фото товара", blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name="Дополнительное фото 1")
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name="Дополнительное фото 2")
    
    # Ссылки на фото из внешних источников (оставляем, но НЕ ИСПОЛЬЗУЕМ)
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на главное фото")
    image_url_2 = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на фото 2")
    image_url_3 = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на фото 3")
    
    available = models.BooleanField(default=True, verbose_name="В наличии")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_sale = models.BooleanField(default=False, verbose_name="Распродажа")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена со скидкой")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['gender']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['collection']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.price}₽"
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def get_sizes_list(self):
        if self.size:
            return [s.strip() for s in self.size.split(',')]
        return []
    
    def get_current_price(self):
        if self.is_sale and self.sale_price:
            return self.sale_price
        return self.price
    
    def get_discount_percent(self):
        if self.is_sale and self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0
    
    # ========== НОВЫЕ МЕТОДЫ - ИГНОРИРУЕМ MEDIA ==========
    
    # В models.py, в классе Product, ЗАМЕНИТЕ все методы get_image_url на эти:

    def get_image_url(self):
        """
        Главное фото - приоритет:
        1. Загруженное через админку изображение (image)
        2. Внешняя ссылка (image_url)
        3. Статический файл по slug
        """
        # Приоритет 1: загруженное через админку фото
        if self.image and self.image.name:
            try:
                return self.image.url
            except:
                pass
        
        # Приоритет 2: внешняя ссылка
        if self.image_url:
            return self.image_url
        
        # Приоритет 3: статический файл по slug
        return f'/static/products/{self.slug}.jpg'
    
    def get_image_2_url(self):
        """Второе фото"""
        if self.image_2 and self.image_2.name:
            try:
                return self.image_2.url
            except:
                pass
        if self.image_url_2:
            return self.image_url_2
        return f'/static/products/{self.slug}-2.jpg'
    
    def get_image_3_url(self):
        """Третье фото"""
        if self.image_3 and self.image_3.name:
            try:
                return self.image_3.url
            except:
                pass
        if self.image_url_3:
            return self.image_url_3
        return None
    
    def has_second_image(self):
        """Проверяет наличие второго фото"""
        if self.image_2 and self.image_2.name:
            return True
        if self.image_url_2:
            return True
        return False
    

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['gender']),
            models.Index(fields=['subcategory']),
            models.Index(fields=['collection']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.price}₽"
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def get_sizes_list(self):
        if self.size:
            return [s.strip() for s in self.size.split(',')]
        return []
    
    def get_current_price(self):
        if self.is_sale and self.sale_price:
            return self.sale_price
        return self.price
    
    def get_discount_percent(self):
        if self.is_sale and self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0
    
    # ========== МЕТОДЫ ДЛЯ ФОТО (без ошибок) ==========
    
    def get_image_url(self):
        """Главное фото"""
        if self.image and self.image.name:
            return self.image.url
        if self.image_url:
            return self.image_url
        # Пробуем найти файл по slug
        return f'/static/shop/products/{self.slug}.jpg'
    
    def get_image_2_url(self):
        """Второе фото - если есть"""
        if self.image_2 and self.image_2.name:
            return self.image_2.url
        if self.image_url_2:
            return self.image_url_2
        # Пробуем найти файл slug-2.jpg
        return f'/static/shop/products/{self.slug}-2.jpg'
    
    def get_image_3_url(self):
        """Третье фото - если есть"""
        if self.image_3 and self.image_3.name:
            return self.image_3.url
        if self.image_url_3:
            return self.image_url_3
        return None  # Третье фото не используем
    
    def has_second_image(self):
        """Проверяет, есть ли второе фото"""
        if self.image_2 and self.image_2.name:
            return True
        if self.image_url_2:
            return True
        return False

class WishlistItem(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name="Ключ сессии")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
    
    def __str__(self):
        return f"{self.product.name} в избранном"


class CartItem(models.Model):
    """Модель элемента корзины"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, null=True, blank=True, verbose_name="Ключ сессии")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    size_selected = models.CharField(max_length=20, blank=True, null=True, verbose_name="Выбранный размер")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = [['user', 'product', 'size_selected'], ['session_key', 'product', 'size_selected']]
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def total_price(self):
        return self.product.get_current_price() * self.quantity


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = (
        ('new', 'Новый заказ'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )
    
    PAYMENT_CHOICES = (
        ('cash', 'Наличными при получении'),
        ('card_courier', 'Картой курьеру'),
        ('card_online', 'Картой онлайн'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к заказу")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name="Способ оплаты")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая сумма")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%d.%m.%Y')}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    """Модель позиции в заказе"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Товар")
    product_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название товара")
    size = models.CharField(max_length=20, blank=True, null=True, verbose_name="Размер")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}" if self.product else "Товар удалён"
    
    def total_price(self):
        return self.price * self.quantity
    
def get_subcategory_display(self):
    """Возвращает читаемое название подкатегории"""
    subcategories = dict(self.SUBCATEGORY_CHOICES)
    return subcategories.get(self.subcategory, self.subcategory or '')

def get_collection_display(self):
    """Возвращает читаемое название коллекции"""
    collections = dict(self.COLLECTION_CHOICES)
    return collections.get(self.collection, self.collection or '')

def get_season_display(self):
    """Возвращает читаемое название сезона"""
    seasons = dict(self.SEASON_CHOICES)
    return seasons.get(self.season, self.season or '')