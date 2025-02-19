from sqlmodel import SQLModel
from .Book import Book, BookBase, BookCreate, BookRead, BookUpdate
from .User import User, UserBase, UserCreate, UserRead
from .UserBook import UserBook

Base = SQLModel

__all__ = [
    "Base",
    "Book",
    "BookBase",
    "BookCreate",
    "BookRead",
    "BookUpdate",
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserBook",
]
