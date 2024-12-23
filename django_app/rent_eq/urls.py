from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RentalViewSet, UserViewSet

router = DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"rental", RentalViewSet)
router.register(r"equipment", EquipmentViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
