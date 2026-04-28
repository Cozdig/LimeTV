# LimeTV Project

DRF проект с генерацией пуш уведомлений.

## Быстрый старт

### Требования
- Docker
- Docker Compose
- Python 3.12+ (для локальной разработки)

### Установка и запуск

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/Cozdig/LimeTV.git
cd LimeTV
```

2. **Установите зависимости**
```bash
pip install -r requirements.txt
```

3. **Создайте файл .env**
```bash
cp .env.sample .env
```

4. **Запустите docker-compose**
```bash
docker-compose up -d --build
```

### Docker команды
```
#Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск с пересборкой
docker-compose down && docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f celery_flower

# Запуск команд внутри контейнера
docker-compose exec web python manage.py <command>
docker-compose exec celery_worker
```

## Структура проекта

```
LimeTV/
├── config/              # Основная папка проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
├── autogen/             # Основное приложение
│   ├── migrations/      # Миграции
│   ├── templates/       # HTML шаблоны
│   │   ├── autogen/ 
│   │   └── ├── info.html 
│   ├── aggregator.py
│   ├── ai.py
│   ├── apps.py
│   ├── filter.py
│   ├── notific_gen.py
│   ├── services.py
│   ├── urls.py
│   ├── tasks.py
│   ├── models.py
│   └── views.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                 # Переменные окружения (не в git)
├── .env.sample          # Пример переменных
├── README.md
├── epg/                 # Папка с информацией о передачах на телеканалах
├── schedule.json        # json файл с сгенерированными пуш уведомлениями
└── manage.py
```

## API Эндпоинты

### **GET /api/get_schedule**

Получает расписание программ за указанную неделю.

**Пример запроса**
```
# Получить расписание на неделю
curl http://{Ip-адрес}:8000/api/get_schedule
```
**Пример ответа**
```
{
    "2026-04-21": {
        "program_1": [{
        "Title": Название программы,
        "Message": Текст анонса/сообщения,
        "Channel": Название канала,
        "Time_zone": Сдвиг часового пояса (относительно UTC),
        "Start_time": Время начала программы (HH:MM),
        "Post_time": Время, когда нужно делать пост]
        },
        {"Title" : Название программы,
        "Message" : Текст анонса/сообщения,
        "Channel": Название канала,
        "Time_zone": Сдвиг часового пояса (относительно UTC),
        "Start_time": Время начала программы (HH:MM),
        "Post_time": Время, когда нужно делать пост]
        }],
        "program_2": [...],
        "program_3": [...]
    },
    "2026-04-22": {...},
    ...
}
```