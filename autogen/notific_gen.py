import json

from autogen.ai import generate_access_token, generate_push


def pushes_generator(result):
    access_token = generate_access_token()
    notifications = {}
    for date, programs in result.items():
        push_list = []
        for program in programs:
            notification = generate_push(access_token, program)
            push_list.append(f"«{notification}». Время {program.start_time}. Канал {program.channel_name.channel_name}")

        notifications[f"{date}"] = push_list

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(notifications, f, ensure_ascii=False, indent=4)