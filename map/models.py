from django.db import models


class ConstructionSite(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")

    STATUS_CHOICES = [
        ("planning", "Планируется"),
        ("construction", "В строительстве"),
        ("completed", "Завершено"),
        ("frozen", "Заморожено"),
    ]
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="construction"
    )

    developer = models.CharField("Застройщик", max_length=200, blank=True)
    start_date = models.DateField("Дата начала", null=True, blank=True)
    completion_date = models.DateField("Плановая дата сдачи", null=True, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    website = models.URLField("Сайт", blank=True)

    class Meta:
        verbose_name = "Строительный объект"
        verbose_name_plural = "Строительные объекты"

    def __str__(self):
        return self.name


class Attraction(models.Model):
    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    category = models.CharField("Категория", max_length=100, blank=True)

    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")

    address = models.CharField("Адрес", max_length=300, blank=True)
    working_hours = models.CharField("Режим работы", max_length=100, blank=True)
    website = models.URLField("Сайт", blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)

    TYPE_CHOICES = [
        ("unknown", "Неизвестно"),
        ("architecture", "Архитектура"),
        ("museum", "Музей"),
        ("park", "Парк"),
        ("nature", "Природа"),
        ("entertainment", "Развлечения"),
        ("sport", "Спорт"),
    ]
    type = models.CharField(
        "Тип достопримечательности",
        max_length=20,
        choices=TYPE_CHOICES,
        default="unknown",
        blank=True,
    )

    class Meta:
        verbose_name = "Достопримечательность"
        verbose_name_plural = "Достопримечательности"

    def __str__(self):
        return self.name
