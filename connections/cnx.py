# from typing import Annotated
# from fastapi import Depends
# from sqlmodel import Session, SQLModel, create_engine
#
#
# sqlite_file_name = "./db/summarize.db"
# sqlite_url = "sqlite:///" + sqlite_file_name
#
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)
#
# def create_db_and_table():
#     SQLModel.metadata.create_all(engine)
#
# def get_session():
#     with Session(engine) as session:
#         yield session
#
# SessionDep = Annotated[Session, Depends(get_session)]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./summarize.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
