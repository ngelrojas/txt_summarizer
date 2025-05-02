from sqlalchemy import Column, Integer, String
from connections.cnx import Base


class Summarize(Base):
    __tablename__ = "summarize"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    text = Column(String)
