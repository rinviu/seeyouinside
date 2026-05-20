import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Создаём НОВОГО пользователя с другим именем
username = 'karina_admin'
password = 'karina2025'
email = 'karina@seeyouinside.ru'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ СОЗДАН: {username} / {password}')
else:
    print(f'⚠️ УЖЕ ЕСТЬ: {username}')

# Выведем всех админов
admins = User.objects.filter(is_superuser=True)
print(f'\n📋 Суперпользователи ({admins.count()}):')
for admin in admins:
    print(f'   - {admin.username}')