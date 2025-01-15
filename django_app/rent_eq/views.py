# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Rental, Equipment
from .serializers import UserSerializer, RentalSerializer, EquipmentSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели User, предоставляющий стандартные действия CRUD.

    Атрибуты:
        queryset (QuerySet): Все объекты User.
        serializer_class (Serializer): Сериализатор для модели User.
    """
    queryset = User.objects.all()  # Получаем все объекты User
    serializer_class = UserSerializer  # Указываем сериализатор для модели User


class RentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Rental, предоставляющий стандартные действия CRUD.

    Атрибуты:
        queryset (QuerySet): Все объекты Rental.
        serializer_class (Serializer): Сериализатор для модели Rental.
    """
    queryset = Rental.objects.all()  # Получаем все объекты Rental
    serializer_class = RentalSerializer  # Указываем сериализатор для модели Rental

    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод создания аренды.

        Проверяет, доступно ли оборудование на указанные даты. 
        Если оборудование занято, возвращает ошибку.

        Аргументы:
            request (Request): Запрос, содержащий данные для создания аренды.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            Response: Ответ с результатом создания аренды или ошибкой.
        """
        equipment_id = request.data.get("equipment")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        # Проверяем, занято ли оборудование на указанные даты
        if Rental.objects.filter(
            equipment_id=equipment_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exists():
            return Response({"error": "Оборудование занято на эти даты"}, status=400)

        return super().create(request, *args, **kwargs)  # Вызываем стандартный метод создания


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Equipment, предоставляющий стандартные действия CRUD.

    Атрибуты:
        queryset (QuerySet): Все объекты Equipment.
        serializer_class (Serializer): Сериализатор для модели Equipment.
    """
    queryset = Equipment.objects.all()  # Получаем все объекты Equipment
    serializer_class = EquipmentSerializer  # Указываем сериализатор для модели Equipment
