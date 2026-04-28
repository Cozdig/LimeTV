import os
from celery import shared_task
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from autogen.filter import filter
from autogen.services import push_priority_count, get_max_priority_programs
from autogen.notific_gen import pushes_generator
from autogen.models import Program

@shared_task
def run_full_pipeline():
    """
    Запускает полный пайплайн: очистка -> импорт -> расчет -> получение топа и списка уведомлений
    """

    # Шаг 0: Очистка БД
    try:
        print("Очистка бд")
        if Program.objects.exists():
            deleted_count, _ = Program.objects.all().delete()
        else:
            print("Таблица уже пуста, пропускаем очистку")
    except Exception as e:
        if "no such table" in str(e).lower():
            print("Таблица Program не существует, пропускаем очистку")
        else:
            return {'status': 'error', 'step': 'cleanup', 'error': str(e)}

    # Шаг 1: Запуск фильтра
    try:
        print("Запуск фильтра")
        filter('epg')
    except Exception as e:
        return {'status': 'error', 'step': 'import', 'error': str(e)}

    # Шаг 2: Расчет приоритетов
    try:
        print("Расчет приоритетов")
        push_priority_count()
    except Exception as e:
        return {'status': 'error', 'step': 'priority', 'error': str(e)}

    # Шаг 3: Получение топа и получение списка уведомлений
    try:
        print("Получение топа")
        result = get_max_priority_programs()
        print("Получение списка уведомлений")
        pushes_generator(result)
        cache.delete('/api/get_schedule/')
    except Exception as e:
        return {'status': 'error', 'step': 'top', 'error': str(e)}
    return {'status': 'success', 'message': 'Пайплайн выполнен, файл отправлен'}