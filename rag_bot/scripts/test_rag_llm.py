import os
import sys
import django

# путь к корню проекта (где лежит manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_map.settings")
django.setup()

from rag_bot.llm.llm import LLM
from rag_bot.services.db_service import get_all_items

def main():
    llm = LLM()
    MODEL_NAME = "map.ConstructionSite"


    objects = get_all_items(MODEL_NAME)
    if not objects:
        print("В базе нет объектов недвижимости!")
        return

    for obj in objects:
        prompt = f"""
Название: {obj.name}
Описание: {obj.description}
Координаты: {obj.latitude}, {obj.longitude}
Статус: {obj.status}
Застройщик: {obj.developer}
Дата начала: {obj.start_date}
Дата завершения: {obj.completion_date}
Телефон: {obj.phone}
Сайт: {obj.website}

Сделай краткое объявление для этого объекта
"""
        answer = llm.generate(prompt)
        print(f"=== {obj.name} ===\n{answer}\n{'-'*50}")

if __name__ == "__main__":
    main()
