import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_map.settings")
django.setup()

from rag_bot.rag_chain import RAGChain

def main():
    if len(sys.argv) < 2:
        print("❗ Укажите вопрос, например:\npython test_rag_llm.py 'какой номер телефона у ЖК Лазурный берег'")
        return

    question = sys.argv[1]
    chain = RAGChain()
    answer = chain.run(question)
    print(f"\n💬 Вопрос: {question}\n🧠 Ответ: {answer}")

if __name__ == "__main__":
    main()