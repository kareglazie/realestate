import os
import sys
import django
import argparse

# Настройка Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_map.settings")
django.setup()

from rag_bot.llm.llm import LLM
from rag_bot.services.db_service import get_all_items

def build_context(objects):
    """
    Формирует текстовый контекст из объектов недвижимости.
    """
    context_lines = []
    for obj in objects:
        line = (
            f"Название: {obj.name}\n"
            f"Описание: {obj.description}\n"
            f"Координаты: {obj.latitude}, {obj.longitude}\n"
            f"Статус: {obj.status}\n"
            f"Застройщик: {obj.developer}\n"
            f"Дата начала: {obj.start_date}\n"
            f"Дата завершения: {obj.completion_date}\n"
            f"Телефон: {obj.phone}\n"
            f"Сайт: {obj.website}\n"
            "---------------------------"
        )
        context_lines.append(line)
    return "\n".join(context_lines)

def main():
    parser = argparse.ArgumentParser(description="Тест RAG с LLM для объектов недвижимости")
    parser.add_argument("question", type=str, help="Вопрос пользователя")
    args = parser.parse_args()
    user_question = args.question

    # Создаём LLM
    llm = LLM()

    # Берём все объекты
    MODEL_NAME = "map.ConstructionSite"
    objects = get_all_items(MODEL_NAME)
    if not objects:
        print("В базе нет объектов недвижимости!")
        return

    # Формируем контекст для RAG
    context = build_context(objects)

    # Полный prompt: контекст + вопрос пользователя
    full_prompt = f"{context}\n\nВопрос пользователя: {user_question}"

    # Получаем ответ LLM
    answer = llm.generate(full_prompt)
    print("=== Ответ LLM ===")
    print(answer)

if __name__ == "__main__":
    main()
