import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from autogen.notific_gen import pushes_generator
from autogen.filter import filter
from autogen.services import push_priority_count, get_max_priority_programs

# Шаг 1: Импорт
# print("1. Импорт JSON...")
# filter('epg')

# Шаг 2: Расчет приоритетов
print("2. Расчет...")
push_priority_count()

# Шаг 3: Получить топ
print("3. Топ программы...")
result = get_max_priority_programs()

# Шаг 4: Получить список уведомлений
pushes_generator(result)