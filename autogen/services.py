from datetime import datetime
from autogen.models import Program

def push_priority_count(programs):
    """Считает приоритет для пуша каждой программы в канале"""
    content_type_scores = {
        #1.0
        "Спорт": 1.0, "Боевик": 1.0, "Экшн": 1.0, "Экшен": 1.0, "Трансляция": 1.0,
        #0.9
        "Новости": 0.9, "Репортаж": 0.9, "Аналитика": 0.9,
        "Интервью": 0.9, "Расследование": 0.9, "Политика": 0.9,
        #0.8
        "Х/ф": 0.8, "Фильм": 0.8, "Концерт": 0.8,
        "Фестиваль": 0.8, "Игра": 0.8, "Чарт": 0.8,
        #0.7
        "М/с": 0.7, "Аниме": 0.7, "Приключения": 0.7,
        "Фэнтези": 0.7, "Фантастика": 0.7, "Триллер": 0.7,
        "Детектив": 0.7, "Криминал": 0.7, "Мистика": 0.7, "Ужасы": 0.7,
        # 0.6
        "Комедия": 0.6, "Ситком": 0.6, "Юмор": 0.6, "Скетч-шоу": 0.6,
        "Шоу": 0.6, "ТВ-шоу": 0.6, "Реалити-шоу": 0.6,
        "Викторина": 0.6, "Ток-шоу": 0.6,
        # 0.5
        "Т/с": 0.5, "Мелодрама": 0.5, "Драма": 0.5,
        "Семейный": 0.5, "М/ф": 0.5, "Сказка": 0.5,
        "Повесть": 0.5, "Мюзикл": 0.5, "Спектакль": 0.5,
        # 0.4
        "Досуг, хобби": 0.4, "Развлечения": 0.4, "Увлечения": 0.4,
        "Культура": 0.4, "Общество": 0.4, "Информация": 0.4,
        "Просвещение": 0.4, "Познавательное": 0.4, "Тележурнал": 0.4, "Обзор": 0.4,
        # 0.3
        "Д/с": 0.3, "Д/ф": 0.3, "Биография": 0.3, "История": 0.3,
        "Наука": 0.3, "Технологии": 0.3, "Путешествия": 0.3, "География": 0.3,
        "Природа": 0.3, "Экология": 0.3, "Медицина": 0.3, "Здоровье": 0.3,
        "Кулинария": 0.3, "Садоводство": 0.3, "Советы": 0.3,
        "Рукоделие": 0.3, "Мода": 0.3, "Танец": 0.3, "Клип": 0.3, "Музыка": 0.3,
        # 0.2
        "Детский": 0.2, "Обучение": 0.2, "Военный": 0.2,
        "Социальный": 0.2, "Экономика": 0.2, "Бизнес": 0.2,
        "Исследование": 0.2, "Короткометражка": 0.2, "Пародия": 0.2, "Конкурс": 0.2,
        # 0.1
        "Реклама": 0.1, "Условное изменение эфира": 0.1,
        "Другое": 0.1, "Эзотерика": 0.1, "Религия": 0.1, "Лотерея": 0.1,
    }

    series_boosts = {
        "Серия": 1.0, "серия": 1.0,
    }

    prime_time_scores = {
        "0": 0.4, "1": 0.4,
        "2": 0.2, "3": 0.2,
        "4": 0.2, "5": 0.2,
        "6": 0.2, "7": 0.2,
        "8": 0.2, "9": 0.2,
        "10": 0.2, "11": 0.2,
        "12": 0.2, "13": 0.2,
        "14": 0.2, "15": 0.2,
        "16": 0.2, "17": 0.7,
        "18": 0.7, "19": 1.0,
        "20": 1.0, "21": 1.0,
        "22": 1.0, "23": 0.4,
    }

    rating_scores = {
        0: 0.2,
        6: 0.2,
        12: 0.5,
        16: 0.8,
        18: 1.0,
    }

    results = []

    for program in programs:
        content_score = 0.0
        categories = program.get('category', [])

        for category in categories:
            if category in content_type_scores:
                content_type_score = max(content_score, content_type_scores[category])

        if 'start_time' in program:
            start_date = datetime.strptime(program['start_time'], '%Y-%m-%d %H:%M:%S')
            hour = start_date.hour

            prime_time_score = prime_time_scores.get(hour)

        age = program.get('age_rating')
        rating_score = rating_scores.get(age)

        series_boost = 0.0
        sub_title = program.get('sub_title', '')
        for key, score in series_boosts.items():
            if key in sub_title:
                series_boost = score
                break



        push_priority = (
                (0.5 * content_type_score) +
                (0.25 * prime_time_score) +
                (0.15 * rating_score) +
                (0.10 * series_boost)
        )

        if "премьера" in program.get("description", "").lower():
            first_priority = True
        else:
            first_priority = False

        results.append({
            'program': program,
            'program_id': program.get("program_id"),
            'priority': round(push_priority, 3),
            'first_priority': first_priority,
            'scores': {
                'content_score': content_score,
                'prime_time_score': prime_time_score,
                'rating_score': rating_score,
                'series_boost': series_boost
            }
        })



    max_priority = max(result['priority'] for result in results)
    top_programs = []

    for result in results:
        if result['priority'] == max_priority and result['first_priority']:
            result['premier'] = True
            top_programs.append(result)
            continue
        elif result['first_priority']:
            result["premier"] = True
            top_programs.append(result)
            continue
        elif result['priority'] == max_priority:
            result["premier"] = False
            top_programs.append(result)
            continue

    for program in top_programs:
        Program.objects.update_or_create(
            program_id=program['program_id'],
            defaults={
                "priority": program["priority"],
                "premier": program["premier"]
            }
        )

