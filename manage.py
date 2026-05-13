#!/usr/bin/env python
"""
Управляющий скрипт Django для проекта SeeYouInside

Использование:
    python manage.py runserver      - запуск сервера разработки
    python manage.py makemigrations - создание миграций
    python manage.py migrate        - применение миграций
    python manage.py createsuperuser - создание администратора
    python manage.py shell          - интерактивная консоль Django
    python manage.py test           - запуск тестов
"""

import os
import sys


def main():
    """
    Основная функция, выполняющая команды управления Django
    """
    # Устанавливаем переменную окружения с настройками
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Выполняем команду
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()