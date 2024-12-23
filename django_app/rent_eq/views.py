# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Rental, Equipment
from .serializers import UserSerializer, RentalSerializer, EquipmentSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def create(self, request, *args, **kwargs):
        equipment_id = request.data.get("equipment")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if Rental.objects.filter(
            equipment_id=equipment_id,
            start_date__lt=end_date,
            end_date__gt=start_date,
        ).exist():
            return Response({"error": "Оборудование занято на эти даты"})

        return super().create(request, *args, **kwargs)


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
