from django.apps import apps

# Пример универсальной функции для получения моделей по имени
def get_model(model_name: str):
    """
    Возвращает модель Django по имени, например 'realestate_map.Property'.
    """
    return apps.get_model(model_name)

# Пример функции для выборки всех объектов
def get_all_items(model_name: str):
    Model = get_model(model_name)
    return Model.objects.all()

# Пример фильтруемой выборки
def get_filtered_items(model_name: str, **filters):
    """
    filters — это kwargs для Django ORM, например: name__icontains="дом"
    """
    Model = get_model(model_name)
    return Model.objects.filter(**filters)
