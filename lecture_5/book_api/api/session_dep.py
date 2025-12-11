"""Database session dependency module.

This module provides FastAPI dependency for managing database sessions.
"""

from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db_config import Session


async def create_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create and manage a database session for a request.

    This async generator creates a new database session, yields it for use
    in the request, and ensures proper cleanup after the request completes.

    Yields:
        AsyncSession: An async database session.
    """
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(create_db_session)]
