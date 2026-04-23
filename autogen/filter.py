import glob
import os.path

from autogen.aggregator import add_data_in_db


multiplex = [
    "Первый канал", "Россия 1", "Матч ТВ", "Телекомпания НТВ", "Пятый канал",
    "Россия К", "Россия 24", "Карусель", "ОТР", "ТВ Центр",
    "РЕН ТВ", "Спас", "СТС", "Домашний", "ТВ-3",
    "Пятница", "Звезда", "МИР-24", "ТНТ", "Муз ТВ",
]

def filter(folder_path):
    json_files = glob.glob(f'{folder_path}/*.json')
    for json_name in json_files:
        if os.path.getsize(json_name) <= 2048:
            continue
        channel_name = os.path.basename(json_name)
        name_without_json = channel_name.replace('.json', '')
        parts = name_without_json.split('_', 1)
        channel_name = parts[1].replace('_', '')
        if channel_name in multiplex:
            continue
        else:
            add_data_in_db(json_name)

