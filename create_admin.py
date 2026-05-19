import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@seeyouinside.ru')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123456!')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Суперпользователь {username} создан!')
else:
    print(f'👤 Суперпользователь {username} уже существует')