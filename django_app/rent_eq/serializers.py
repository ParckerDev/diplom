from rest_framework import serializers
from .models import Equipment, User, Rental


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = User


class EquipmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Equipment


class RentalSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Rental
