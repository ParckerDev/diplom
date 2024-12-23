from core import Base
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    telephone_number: Mapped[str] = mapped_column(String(12), nullable=False)

    def __str__(self):
        return f"{self.username} | {self.telephone_number}"


class Equipment(Base):
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    discription: Mapped[str] = mapped_column(String(250))

    def __str__(self):
        return self.name


class Rental(Base):
    equipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipments.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    start_date: Mapped[str] = mapped_column(Date)
    end_date: Mapped[str] = mapped_column(Date)

    equipment = relationship("Equipment")
    user = relationship("User")
