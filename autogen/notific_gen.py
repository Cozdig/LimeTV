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
all_timezones = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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
        push_list = {}
        num = 0
        for program in programs:
            num += 1
            channel_name = program.channel_name.channel_name
            timezone_notifications = []
            if channel_name in timezones.keys():
                notification = generate_push(access_token, program)
                for hour_offset in timezones.get(channel_name):
                    local_time = program.start_time + timedelta(hours=hour_offset)
                    timezone_notifications.append({"Title": program.title, "Message": notification.replace("(время начала)", format_time(local_time)), "Channel": channel_name, "Time_zone": hour_offset, "Start_time": format_time(local_time), "Post_time": format_time(local_time - timedelta(minutes=20))})
                push_list[f"program_{num}"] = timezone_notifications
            else:
                notification = generate_push(access_token, program)
                for hour_offset in all_timezones:
                    local_time = program.start_time + timedelta(hours=hour_offset)
                    timezone_notifications.append({"Title": program.title, "Message": notification.replace("(время начала)", format_time(local_time)), "Channel": channel_name, "Time_zone": hour_offset, "Start_time": format_time(local_time), "Post_time": format_time(local_time - timedelta(minutes=20))})
                push_list[f"program_{num}"] = timezone_notifications
        notifications[f"{date}"] = push_list

    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=4)
