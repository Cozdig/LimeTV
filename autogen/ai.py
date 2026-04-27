import requests
from dotenv import load_dotenv
import os
import time

# Импортирование api-ключа из .env файла
load_dotenv(override=True)
AUTH_KEY = os.getenv("AUTH_KEY")


def generate_access_token(max_retries=5, retry_delay=4):
    """
    Генерирует Access token с автоматическими повторными попытками при ошибке.
    """
    for attempt in range(1, max_retries + 1):
        try:
            auth_response = requests.post(
                "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                headers={
                    "Authorization": f"Basic {AUTH_KEY}",
                    "RqUID": "6f0b1a2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"scope": "GIGACHAT_API_PERS"},
                verify=False,
                timeout=10
            )

            auth_response.raise_for_status()

            response_data = auth_response.json()
            if "access_token" not in response_data:
                raise ValueError(f"Access token not found in response: {response_data}")

            print(f"Токен получен (попытка {attempt})")
            return response_data["access_token"]

        except requests.exceptions.Timeout as e:
            print(f"Таймаут при получении токена (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Не удалось получить токен после {max_retries} попыток (таймаут)")

        except requests.exceptions.ConnectionError as e:
            print(f"Ошибка подключения (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay * 2)
            else:
                raise Exception(f"Не удалось подключиться к серверу после {max_retries} попыток")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Не удалось получить токен после {max_retries} попыток")

        except (KeyError, ValueError) as e:
            print(f"Ошибка в ответе сервера (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Некорректный ответ сервера после {max_retries} попыток")

        except Exception as e:
            print(f"Неизвестная ошибка (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"🔄 Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Критическая ошибка после {max_retries} попыток: {e}")

    raise Exception(f"Все {max_retries} попытки получения токена не удались")

def generate_push(access_token, program, time, max_retries=5, retry_delay=4):
    """
    Отправляет промпт на ИИ GigaChat, нужные данные берутся из модели
    """
    prompt = f"""
    Сгенерируй короткое push-уведомление (до 20 слов).

    Примеры уведомлений:
    1. Включай новый сериал🔥 В 22:00 на Первом канале военная драма → «В парке Чаир»
    2. Новый канал «КиноКульт» 🎥 Легендарные боевики, драмы и триллеры — без паузы!
    3. Спорт дома 🏡 Фитнес, йога, танцы. Тренировки для всех уровней. Включай «Живи активно»
    4. Нажми на меня И смотри в 19:00 на «Феникс+Кино» мелодраму о тайнах прошлого 💔«Холодное блюдо»
    5. Кино без перерыва 🍿 Лучшие фильмы и сериалы 24/7 на новом канале ⭐️«Hollywood HD»
    6. Спорт дома 🏡 Фитнес, йога, танцы. Тренировки для всех уровней. Включай «Живи активно»
    7. Выжить любой ценой 💥 Пилот против опасного острова и бандитов ✈️«Крушение» в 20:35 на ТВ21
    8. Отправляемся к звездам✨ Включай в 15:05 МСК "Тайны Галактики"→ Смотри 🪐"Кино про космос"
    9. Каждое дело - как рецепт!  «Кулинар»🔎 детективный сериал в 18:30 на «Мир сериала»
    10. Никаких вопросов... Включай «Кино и Жизнь» в 19:10. Смотри криминальный триллер 😈«Гангстер, коп и дьявол» 
    11. Вау, какой😯 Детективный триллер "Воздушный маршал" в 20:45 на канале "Hollywood HD" 
    12. Как строят плавучие дворцы ⚓️ «Создавая круизные лайнеры» → смотри документальный фильм в 14:00 на Океан HD
    13. Место, откуда не сбежать… «Забытый остров»🔍👀премьера детектива в 17:10 на «ТВ Центр»
    14. Кино для тебя👇История про настоящих мафиози «Славные парни» в 21:50 на канале «КиноКульт»
    15. 40 лет спустя… «Чернобыль. Как это было» → документальный фильм в 12:15 на Первом канале 
    16. Кот, мышь и немного хаоса 😸 Мультфильм «Коты Эрмитажа»🐾 в 15:10 на канале «Мультиландия»
    17. Любовь, люди и пёсики 🐶 «Хвостатый переполох» в 20:05 на «Kinoliving». Трогательные истории и немного хаоса 🐾

    Дано:
    Канал: {program.channel_name.channel_name}
    Название: {program.title}
    Описание: {program.description}
    Время: {time}

    Стиль: как в примерах (живо, с эмоцией, с emoji подходящими к тексту)
    """

    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "GigaChat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 150
                },
                verify=False,
                timeout=10
            )

            response.raise_for_status()
            response_data = response.json()

            if "choices" not in response_data or not response_data["choices"]:
                raise ValueError(f"Неверная структура ответа: {response_data}")

            push_text = response_data["choices"][0]["message"]["content"]

            if not push_text or not push_text.strip():
                raise ValueError("Получен пустой ответ от ИИ")

            print(f"Пуш сгенерирован (попытка {attempt})")
            return push_text.strip()

        except requests.exceptions.Timeout as e:
            last_error = e
            print(f"Таймаут (попытка {attempt}/{max_retries})")

        except requests.exceptions.ConnectionError as e:
            last_error = e
            print(f"Ошибка подключения (попытка {attempt}/{max_retries})")
            retry_delay *= 2

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Токен истёк! Получите новый access_token")
            last_error = e
            print(f"HTTP {response.status_code} (попытка {attempt}/{max_retries})")

        except (KeyError, IndexError, ValueError) as e:
            last_error = e
            print(f"Ошибка ответа ИИ (попытка {attempt}/{max_retries})")

        except Exception as e:
            last_error = e
            print(f"Ошибка (попытка {attempt}/{max_retries})")

        # Ждём перед следующей попыткой
        if attempt < max_retries:
            print(f"Повтор через {retry_delay} сек...")
            time.sleep(retry_delay)

    # Все попытки исчерпаны
    raise Exception(f"Не удалось сгенерировать пуш после {max_retries} попыток. Последняя ошибка: {last_error}")
