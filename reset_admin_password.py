"""
Скрипт для сброса пароля суперпользователя на Render
"""

import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Импортируем Django после настроек
import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Удаляем старого админа если есть
User.objects.filter(username='admin').delete()

# Создаём нового с простым паролем
user = User.objects.create_superuser(
    username='admin',
    email='admin@seeyouinside.ru',
    password='admin123'
)

print('✅ Суперпользователь создан!')
print('   Логин: admin')
print('   Пароль: admin123')