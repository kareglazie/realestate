from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from map.models import ConstructionSite

INDEX_REBUILD_KEY = 'faiss_index_needs_rebuild'

@receiver([post_save, post_delete], sender=ConstructionSite)
def mark_index_for_rebuild(sender, instance, **kwargs):
    """
    Помечает индекс для перестройки при изменении данных.
    Реальная перестройка произойдет при следующем запросе к RAG.
    """
    cache.set(INDEX_REBUILD_KEY, True, timeout=None)
    print(f"🔄 Индекс помечен для перестройки (изменен объект: {instance.name})")