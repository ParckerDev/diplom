from sqlalchemy import MetaData, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from . import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
