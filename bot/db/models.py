"""Models"""

from sqlalchemy import (
    Integer,
    String,
    Text,
    Column,
    ForeignKey,
    Numeric,
    Time,
    Boolean,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UserItem(Base):
    __tablename__ = "user_item"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    item_id = Column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)
    user = relationship("User", back_populates="items")
    item = relationship("Item", back_populates="users")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    items = relationship("Item", back_populates="category")


class ItemPhoto(Base):
    __tablename__ = "item_photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(150), nullable=False)
    item_id = Column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)
    item = relationship("Item", back_populates="photos")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    category = relationship("Category", back_populates="items")
    orders = relationship("Order", back_populates="item")
    photos = relationship("ItemPhoto", back_populates="item")
    users = relationship("UserItem", back_populates="item")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"))
    item = relationship("Item", back_populates="orders")
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="orders")
    paid = Column(Boolean, default=False, nullable=False)
    summ = Column(Numeric(12, 2), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=False)
    items = relationship("UserItem", back_populates="user")
    orders = relationship("Order", back_populates="user")
