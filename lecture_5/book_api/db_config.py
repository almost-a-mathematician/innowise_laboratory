from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(primary_key=True)


DB_NAME: str = 'book_collection.db'

DB_URL: str = f'sqlite+aiosqlite:///{DB_NAME}'

engine = create_async_engine(DB_URL, echo=True)

Session = async_sessionmaker(engine)