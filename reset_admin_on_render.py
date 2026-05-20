"""
Скрипт для сброса пароля и создания админа на Render
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("=" * 50)
print("Проверка суперпользователя...")
print("=" * 50)

# Удаляем старого админа
User.objects.filter(username='admin').delete()

# Создаём нового
user = User.objects.create_superuser(
    username='admin',
    email='admin@seeyouinside.ru',
    password='admin123'
)

print(f"✅ Суперпользователь создан!")
print(f"   Логин: admin")
print(f"   Пароль: admin123")
print("=" * 50)