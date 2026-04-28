import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class ScheduleJsonAPIView(View):
    @method_decorator(cache_page(3600))
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'schedule.json')

        if not os.path.exists(file_path):
            return JsonResponse(
                {'error': 'Файл с расписанием ещё не сгенерирован. Задача выполняется по воскресеньям.'},
                status=404
            )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Ошибка чтения JSON файла'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class InfoView(View):
    def get(self, request):
        return render(request, 'autogen/info.html')