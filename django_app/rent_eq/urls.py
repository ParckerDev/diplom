from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RentalViewSet, UserViewSet

# Создаем экземпляр маршрутизатора по умолчанию
router = DefaultRouter()

# Регистрируем маршруты для представлений (ViewSet) пользователей, аренды и оборудования
router.register(r"users", UserViewSet)        # Маршрут для пользователей
router.register(r"rental", RentalViewSet)      # Маршрут для аренды
router.register(r"equipment", EquipmentViewSet) # Маршрут для оборудования

# Определяем URL-шаблоны для приложения
urlpatterns = [
    path("", include(router.urls)),  # Включаем маршруты, определенные в маршрутизаторе
]
