import os
import shutil
import numpy as np
from langchain.chains import RetrievalQA
import faiss
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.docstore.in_memory import InMemoryDocstore
from rag_bot.llm import LLM
from rag_bot.services.db_service import get_all_items

from django.core.cache import cache

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")
MODEL_NAME_FOR_DOCS = "map.ConstructionSite"

class RAGChain:
    def __init__(self):
        self.llm = LLM()
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        INDEX_REBUILD_KEY = 'faiss_index_needs_rebuild'
        
        if cache.get(INDEX_REBUILD_KEY) and os.path.exists(INDEX_PATH):
            print("🔄 Обнаружены изменения в БД. Пересоздаю индекс...")
            shutil.rmtree(INDEX_PATH)
            cache.delete(INDEX_REBUILD_KEY)

        if os.path.exists(INDEX_PATH):
            self.vector_store = FAISS.load_local(
                INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self.build_index()

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Ты помощник отдела недвижимости. Используй контекст, чтобы ответить на вопрос пользователя.\n\n"
                "Контекст:\n{context}\n\n"
                "Вопрос: {question}\n\n"
                "Ответ:"
            )
        )

        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            ),
            return_source_documents=False,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def build_index(self):
        items = get_all_items(MODEL_NAME_FOR_DOCS)
        documents = []
        for item in items:
            lines = [f"Название: {item.name}"]
            if hasattr(item, 'description') and item.description:
                lines.append(f"Описание: {item.description}")
            if hasattr(item, 'latitude') and hasattr(item, 'longitude') and item.latitude and item.longitude:
                lines.append(f"Координаты: {item.latitude}, {item.longitude}")
            if hasattr(item, 'status') and item.status:
                lines.append(f"Статус: {item.status}")
            if hasattr(item, 'developer') and item.developer:
                lines.append(f"Застройщик: {item.developer}")
            if hasattr(item, 'start_date') and item.start_date:
                lines.append(f"Дата начала: {item.start_date}")
            if hasattr(item, 'completion_date') and item.completion_date:
                lines.append(f"Дата завершения: {item.completion_date}")
            if hasattr(item, 'phone') and item.phone:
                lines.append(f"Телефон: {item.phone}")
            if hasattr(item, 'website') and item.website:
                lines.append(f"Сайт: {item.website}")
            
            text = "\n".join(lines)
            documents.append(text)

        if not documents:
            raise ValueError("Нет данных для индексации! Проверь, есть ли объекты в базе данных.")
        
        d = len(self.embeddings.embed_query("test"))
        index = faiss.IndexHNSWFlat(d, 32)
        vectors = np.array([self.embeddings.embed_query(d) for d in documents], dtype="float32")
        index.add(vectors)

        docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)})
        index_to_docstore_id = {i: str(i) for i in range(len(documents))}

        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id
        )

        self.vector_store.save_local(INDEX_PATH)
        print(f"✅ Индекс создан: {len(documents)} документов")

    def run(self, question: str):
        try:
            return self.chain.invoke(question)
        except Exception as e:
            return f"Ошибка при обработке запроса: {str(e)}"