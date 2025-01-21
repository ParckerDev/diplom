from core import Base
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """
    Модель пользователя.

    Атрибуты:
        username (str): Уникальное имя пользователя.
        email (str): Уникальный адрес электронной почты.
        password (str): Пароль пользователя.
        telephone_number (str): Номер телефона пользователя.
    """

    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    telephone_number: Mapped[str] = mapped_column(String(12), nullable=False)

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        Возвращает:
            str: Строка, содержащая имя пользователя и номер телефона.
        """
        return f"{self.username} | {self.telephone_number}"


class Equipment(Base):
    """
    Модель оборудования.

    Атрибуты:
        name (str): Уникальное название оборудования.
        discription (str): Описание оборудования.
    """

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    discription: Mapped[str] = mapped_column(String(250))

    def __str__(self):
        """
        Возвращает строковое представление оборудования.

        Возвращает:
            str: Название оборудования.
        """
        return self.name


class Rental(Base):
    """
    Модель аренды.

    Атрибуты:
        equipment_id (int): Идентификатор арендуемого оборудования.
        user_id (int): Идентификатор пользователя, который арендует оборудование.
        start_date (str): Дата начала аренды.
        end_date (str): Дата окончания аренды.
    """

    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipments.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    start_date: Mapped[str] = mapped_column(Date)
    end_date: Mapped[str] = mapped_column(Date)

    equipment = relationship("Equipment")
    user = relationship("User")
