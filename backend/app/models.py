from contextlib import asynccontextmanager
from asyncio import current_task
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_scoped_session,
)
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .utils import db_set_up

db_config = db_set_up()

Base = declarative_base()

engine_uri = 'mysql+aiomysql://%s:%s@%s/%s?charset=utf8' % (
    db_config["DB_USER_NAME"],
    db_config["DB_USER_PASSWD"],
    db_config["DB_HOST"],
    db_config["DB_NAME"],
)

engine = create_async_engine(
    engine_uri,
    pool_recycle=3600,
)

async_session_factory = sessionmaker(bind=engine, class_=AsyncSession)

session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


# async def _async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     await engine.dispose()

class Users(Base):
    __tablename__ = "users"
    id: str = Column(String, primary_key=True, index=True)
    name: Optional[str] = Column(String, nullable=True)
    password: str = Column(String, nullable=False)


class CodeM(Base):
    __tablename__ = "tb_code_m"
    C_ID: str = Column(String, primary_key=True, index=True)
    C_PARENT_ID: Optional[str] = Column(String, nullable=True, index=True)
    C_NAME: Optional[str] = Column(String, nullable=True)
    C_ENG_NAME: Optional[str] = Column(String, nullable=True)
    C_DESCRIPTION: Optional[str] = Column(String, nullable=True)

    # CODE_PROBLEMS: list["CodeProblem"] = relationship(
    #     "CodeProblem", lazy="joined", backref="CodeM")


class CodeProblem(Base):
    __tablename__ = "tb_code_problem"
    CP_SEQ: int = Column(Integer, primary_key=True, index=True)
    CP_CATEGORY_CD: str = Column(String, nullable=False, index=True)
    CP_TITLE: str = Column(String, nullable=False)
    CP_LEVEL_CD: str = Column(String, nullable=False)
    CP_CONTENT: Optional[str] = Column(String, nullable=True)
    CP_TAG: str = Column(String, nullable=False)
    CP_LAPTIME: DateTime = Column(
        DateTime(timezone=True), nullable=True, server_default=func.now())
