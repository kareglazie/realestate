from django.core.management.base import BaseCommand
from rag_bot.services.db_service import get_all_items
from rag_bot.llm.llm import LLM

class Command(BaseCommand):
    help = "Запускает тест RAG с локальной LLM"

    def handle(self, *args, **options):
        llm = LLM()
        # выбираем все объекты недвижимости
        objects = get_all_items("map.MapConstructionsite")  # проверь app_label через shell
        if not objects:
            self.stdout.write("В базе нет объектов недвижимости!")
            return

        for obj in objects:
            prompt = f"""
Объект недвижимости:
Название: {obj.name}
Описание: {obj.description}
Координаты: {obj.latitude}, {obj.longitude}
Статус: {obj.status}
Застройщик: {obj.developer}
Дата начала: {obj.start_date}
Дата завершения: {obj.completion_date}
Телефон: {obj.phone}
Сайт: {obj.website}

Сделай краткое описание для объявления.
                """
            response = llm.generate(prompt)
            self.stdout.write(f"=== {obj.name} ===\n{response}\n")
