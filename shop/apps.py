"""
Конфигурация приложения shop
"""

from django.apps import AppConfig


class ShopConfig(AppConfig):
    """
    Класс конфигурации приложения shop
    """
    # Тип поля по умолчанию для автоинкрементных полей
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Имя приложения (используется в INSTALLED_APPS)
    name = 'shop'
    
    # Человеко-читаемое название приложения
    verbose_name = 'Интернет-магазин SeeYouInside'
    
    def ready(self):
        """
        Метод, вызываемый при загрузке приложения
        Здесь можно регистрировать сигналы
        """
        # Импортируем сигналы (если будут добавлены)
        # import shop.signals
        pass