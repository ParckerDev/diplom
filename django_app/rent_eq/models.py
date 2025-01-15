from django.db import models

# Create your models here.


class User(models.Model):
    """
    Модель пользователя, представляющая информацию о пользователе системы.

    Атрибуты:
        username (str): Уникальное имя пользователя (максимум 150 символов).
        telephone_number (str): Уникальный номер телефона (максимум 12 символов).
        email (str): Уникальный адрес электронной почты.
        password (str): Пароль пользователя (максимум 128 символов).
    """
    username = models.CharField(max_length=150, unique=True)
    telephone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        """Возвращает строковое представление пользователя - его имя."""
        return self.username


class Equipment(models.Model):
    """
    Модель оборудования, представляющая информацию об оборудовании.

    Атрибуты:
        name (str): Уникальное название оборудования (максимум 150 символов).
        description (str): Описание оборудования.
    """
    name = models.CharField(max_length=150, unique=True)
    discription = models.TextField()

    def __str__(self):
        """Возвращает строковое представление оборудования - его название."""
        return self.name


class Rental(models.Model):
    """
    Модель аренды, представляющая информацию об аренде оборудования пользователем.

    Атрибуты:
        equipment (ForeignKey): Ссылка на модель Equipment, указывающая на арендуемое оборудование.
        user (ForeignKey): Ссылка на модель User, указывающая на пользователя, арендующего оборудование.
        start_date (date): Дата начала аренды.
        end_date (date): Дата окончания аренды.
    """
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        """Возвращает строковое представление аренды, включая информацию об оборудовании, пользователе и дате окончания аренды."""
        return f"Equipment: {self.equipment.name} | User: {self.user.username} | End_date: {self.end_date}"
