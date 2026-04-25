import json
from datetime import timedelta

from autogen.ai import generate_access_token, generate_push

timezones = {
    "СТС-Love": [0, 2, 4],
    "Че": [0, 2, 4, 7],
    "Ю": [0, 2, 7],
    "2x2": [0, 2, 4],
    "Солнце": [0, 2, 7],
    "Суббота": [0, 2, 4],
}

def format_time(dt):
    """
    Форматирует объект Date в нужный формат Часы:Минуты
    """
    return dt.strftime("%H:%M")

def pushes_generator(result):
    """
   Генерирует список уведомлений с временем начала, названием канала и временем отправки уведомления,
   после записывает все уведомления в data.json
   """
    access_token = generate_access_token()
    notifications = {}
    for date, programs in result.items():
        push_list = []
        for program in programs:
            channel_name = program.channel_name.channel_name
            if channel_name in timezones.keys():
                timezone_notifications = []
                for hour_offset in timezones.get(channel_name):
                    local_time = program.start_time + timedelta(hours=hour_offset)
                    notification = generate_push(access_token, program, local_time)
                    timezone_notifications.append(f"«{notification}». Начало программы по МСК +{hour_offset} - {format_time(local_time)}. Канал - {channel_name}. Пуш уведомления в - {format_time(local_time - timedelta(minutes=20))} по местному времени")
                push_list.append(timezone_notifications)
            else:
                notification = generate_push(access_token, program, program.start_time)
                push_list.append(f"«{notification}». Начало программы - {format_time(program.start_time)}. Канал - {channel_name}. Пуш уведомления в - {format_time(program.start_time - timedelta(minutes=20))}")



        notifications[f"{date}"] = push_list

    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=4)

