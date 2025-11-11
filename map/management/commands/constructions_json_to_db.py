import json
from django.core.management.base import BaseCommand
from map.models import ConstructionSite
from datetime import datetime

class Command(BaseCommand):
    help = 'Import construction sites from JSON file (update existing + add new)'
    
    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')
        parser.add_argument(
            '--key-field', 
            type=str, 
            default='name',
            help='Field to match existing records (default: name)'
        )
    
    def handle(self, *args, **options):
        json_file = options['json_file']
        key_field = options['key_field']
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            created_count = 0
            updated_count = 0
            errors = []
            
            for index, item in enumerate(data):
                try:
                    defaults = {
                        'description': item.get('description', ''),
                        'latitude': float(item['latitude']),
                        'longitude': float(item['longitude']),
                        'status': item.get('status', 'construction'),
                        'developer': item.get('developer', ''),
                        'start_date': self.parse_date(item.get('start_date')),
                        'completion_date': self.parse_date(item.get('completion_date')),
                        'phone': item.get('phone', ''),
                        'website': item.get('website', ''),
                    }
                    
                    lookup_key = {key_field: item[key_field]}
                
                    obj, created = ConstructionSite.objects.update_or_create(
                        **lookup_key,
                        defaults=defaults
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f"Создан: {item[key_field]}")
                    else:
                        updated_count += 1
                        self.stdout.write(f"Обновлен: {item[key_field]}")
                        
                except KeyError as e:
                    errors.append(f"Строка {index}: Отсутствует поле {e}")
                except Exception as e:
                    errors.append(f"Строка {index}: {e}")
            
            self.stdout.write(self.style.SUCCESS(
                f'Данные добавлены в базу'
                f'Создано новых: {created_count}\n'
                f'Обновлено существующих: {updated_count}\n'
                f'Ошибок: {len(errors)}'
            ))
            
            if errors:
                self.stdout.write("Ошибки:")
                for error in errors:
                    self.stdout.write(self.style.ERROR(f"{error}"))
                    
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Файл не найден'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Ошибка формата JSON'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
    
    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            try:
                return datetime.strptime(date_str, '%d.%m.%Y').date()
            except:
                return None