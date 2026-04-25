import glob
import os.path

from autogen.aggregator import add_data_in_db

multiplex = [
    "Первый канал", "Россия-1", "Матч ТВ", "Телекомпания НТВ", "Пятый канал",
    "Россия - К", "Россия - 24", "Детско-юношеский телеканал _Карусель_", "Общественное телевидение России", "ТВ Центр",
    "РЕН ТВ", "Спас", "СТС", "Домашний", "ТВ-3",
    "Пятница", "Звезда", "МИР-24", "ТНТ", "МУЗ-ТВ",
]

white_list = ["360", "РЖД ТВ", "RT", "Красная линия", "7tv",
              "Калейдоскоп ТВ", "8 Канал", "Точка ТВ", "Нано", "RTД HD",
              "Шансон", "O2TV", "Министерство Идей", "Смайл ТВ", "ПРО БИЗНЕС", "Вместе-РФ",
              "Центральное ТВ", "Ратник", "Известия", "Старт", "Пес и Ко",
              "Продвижение", "Седьмой канал", "Крик ТВ", "Суббота", "UNIVER TV",
              "ЕГЭ", "Детский Мир", "Первый Вегетарианский", "Открытый мир", "ЛДПР ТВ",
              "Жар Птица", "RUSSIAN MUSIC BOX", "Радость моя", "Fashion TV", "Надежда",
              "СТС-Love", "Жара", "МузСоюз", "Советские мультфильмы", "Советское кино",
              "Океан HD", "Мото Драйв", "Страна FM", "Большая Азия", "Диалоги о рыбалке",
              "360 Новости", "КиноСезон", "Терра Инкогнита", "Неизвестная планета", "Дума ТВ",
              "ТВ ПРНК", "CGTN", "CGTN Русский", "Детское кино", "Экстра ТВ",
              "SONGTV Russia", "SONGTV Armenia", "TV BRICS", "Телеканал народной музыки", "Светлое ТВ",
              "RT DOC Eng", "RT Eng", "RT France", "Arirang", "Здоровье",
              "Живи Активно", "Живая природа", "Глазами туриста", "Тайны Галактики", "Загородная Жизнь",
              "BRIDGE DELUXE", "BRIDGE ШЛЯГЕР", "РБК", "BRIDGE ROCK", "Travelxp HD",
              "Clubbing TV HD", "Союз", "ОСН ТВ", "Kinoliving", "World Fashion Channel HD",
              "СОЛОВЬЁВLIVE", "Три Ангела", "FON Music", "Телеканал HHQ", "Успех",
              "Мегаполис Югра", "Феникс_ Кино", "Ю", "Наше старое кино", "LUXURY",
              "BRIDGE", "BABY TIME", "Horror TV", "Quadro", "Старт Триумф",
              "АРТ", "Че", "ТНТ4", "Музыка Мода ТВ", "BRIDGE HITS",
              "ТВ-21", "Неизвестная Россия", "ЮТВ", "BRIDGE Фрэш", "2x2",
              "Europa Plus TV", "RT Arabic", "Телеканал ТБВ", "LEOMAX24", "RT Español",
              "Мир сериала", "Мы", "Аппетитный", "LIVETVAZ", "RT Deutsch",
              "Конгресс ТВ", "AIVA", "ВКУС", "ЭХ_", "ПЛЮС_МИНУС 16",
              "Волейбол", "BRIDGE ЭТНО", "Кино и Жизнь", "Balapan International", "Хочу всё знать_",
              "Союзный", "RU.TV", "BRIDGE РУССКИЙ ХИТ", "BRIDGE CLASSIC", "Солнце",
              "МИР", "Мультиландия"]


def filter(folder_path):
    """
    Фильтрует каналы по белому списку
    """
    json_files = glob.glob(f'{folder_path}/*.json')
    for json_name in json_files:
        if os.path.getsize(json_name) <= 2048:
            continue
        channel_name = os.path.basename(json_name)
        name_without_json = channel_name.replace('.json', '')
        parts = name_without_json.split('_', 1)
        channel_name = parts[1].replace('_', '')
        if channel_name in white_list:
            add_data_in_db(json_name)
        else:
            continue
