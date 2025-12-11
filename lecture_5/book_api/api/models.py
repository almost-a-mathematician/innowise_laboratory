from db_config import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Book(Base):
    __tablename__ = 'books'
    
    title: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    year: Mapped[int] = mapped_column(nullable=True, index=True)