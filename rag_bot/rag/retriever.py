from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from rag_bot.services.db_service import get_all_items

class RAGRetriever:
    """
    Класс для интеграции с векторной базой документов (RAG).
    """
    def __init__(self, index_path: str, model_name_for_docs: str):
        """
        index_path: путь к сохранённому FAISS индексу
        model_name_for_docs: Django модель, из которой берутся документы для векторизации
        """
        self.index_path = index_path
        self.model_name_for_docs = model_name_for_docs
        self.embeddings = OpenAIEmbeddings()  # можно заменить на любую локальную векторизацию
        self.vector_store = FAISS.load_local(index_path, self.embeddings)

    def update_index(self):
        """
        Обновляет индекс из текущих данных в базе.
        """
        docs = get_all_items(self.model_name_for_docs)
        documents = [str(doc) for doc in docs]  # превращаем объекты в строки
        self.vector_store.add_texts(documents)
        self.vector_store.save_local(self.index_path)

    def search(self, query: str, top_k: int = 5):
        """
        Поиск похожих документов по запросу.
        """
        return self.vector_store.similarity_search(query, k=top_k)
