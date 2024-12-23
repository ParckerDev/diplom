from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    telephone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Equipment(models.Model):
    name = models.CharField(max_length=150, unique=True)
    discription = models.TextField()

    def __str__(self):
        return self.name


class Rental(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Equipment: {self.equipment.name} | User: {self.user.username} | End_date: {self.end_date}"
