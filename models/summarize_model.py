# from sqlmodel import Field, Session, SQLModel, create_engine, select
#
#
# class Summarize(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     name_doc: str = Field(nullable=False)
#     name_session: str = Field(nullable=False)
from sqlalchemy import Column, Integer, String
from connections.cnx import Base


class Summarize(Base):
    __tablename__ = "summarize"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    text = Column(String)
    model = Column(String)
    provider = Column(String)
