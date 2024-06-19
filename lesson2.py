from datetime import datetime

from sqlalchemy import BIGINT, VARCHAR, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship
from sqlalchemy.sql.functions import now, func
from typing_extensions import Annotated, Optional


class Base(DeclarativeBase):
    pass






class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"





intpk = Annotated[int, mapped_column(Integer, primary_key=True, nullable=False)]

user_fk = Annotated[int, mapped_column(BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL', nullable=True))]

str_255 = Annotated[str, mapped_column(VARCHAR(255))]


class TelegramUser(Base):
    telegram_id: Mapped[int] = mapped_column(
        BIGINT, nullable=False, primary_key=True
    )
    full_name: Mapped[Optional[str_255]]
    username: Mapped[str_255]
    language: Mapped[str_255]
    referrer_id: Mapped[Optional[user_fk]]


class Product[Base, TableNameMixin, TimeStampMixin]:
    product_id: Mapped[intpk]
    title: Mapped[str_255]
    description: Mapped[Optional[str]]

class Order[Base, TableNameMixin, TimeStampMixin]:
    order_id: Mapped[intpk]
    user_id: Mapped[user_fk]


class OrderProduct(Base):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.order_id', ondelete = "CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.product_id', ondelete = "RESTRICT"), primary_key=True)
    quantity: Mapped[int]