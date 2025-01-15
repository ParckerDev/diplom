from rest_framework import serializers
from .models import Equipment, User, Rental


class BaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для моделей, наследующий от ModelSerializer.

    Этот сериализатор автоматически включает все поля модели в сериализацию и десериализацию.
    """
    class Meta:
        fields = "__all__"


class UserSerializer(BaseSerializer):
    """
    Сериализатор для модели User.

    Используется для преобразования экземпляров модели User в JSON и обратно.
    """
    class Meta(BaseSerializer.Meta):
        model = User


class EquipmentSerializer(BaseSerializer):
    """
    Сериализатор для модели Equipment.

    Используется для преобразования экземпляров модели Equipment в JSON и обратно.
    """
    class Meta(BaseSerializer.Meta):
        model = Equipment


class RentalSerializer(BaseSerializer):
    """
    Сериализатор для модели Rental.

    Используется для преобразования экземпляров модели Rental в JSON и обратно.
    """
    class Meta(BaseSerializer.Meta):
        model = Rental
