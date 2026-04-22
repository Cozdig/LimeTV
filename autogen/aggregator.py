import json
import os.path

from autogen.models import Channel, Program
from datetime import datetime


def add_data_in_db(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if not data or isinstance(data, list):
            return
        channel_name = os.path.basename(file_name)
        name_without_json = channel_name.replace('.json', '')
        parts = name_without_json.split('_', 1)
        channel_name = parts[1]

        channel, _ = Channel.objects.get_or_create(channel_name=channel_name)

        for day in data.get('epg', []):
            if not data.get('epg'):
                return
            date = datetime.strptime(day['date'],'%d.%m.%Y').date()

            for program in day.get('data'):
                Program.objects.update_or_create(
                    program_id=program['id'],
                    defaults={
                        'channel_name': channel,
                        'date': date,
                        'duration': (program.get('timestop', 0) - program.get('timestart', 0)) // 60,
                        'title': program.get('title', ''),
                        'description': program.get('desc', ''),
                        'age_rating': program.get('rating', 0),
                        'sub_title': program.get('sub_title', ''),
                        'category': ', '.join(program.get('category', [])),
                        'start_time': datetime.strptime(program['mskdatetimestart'], '%Y-%m-%d %H:%M:%S')
                    }
                )

