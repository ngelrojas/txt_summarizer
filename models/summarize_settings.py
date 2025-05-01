from sqlalchemy import Column, Integer, String
from connections.cnx import Base


class SummarizeSettings(Base):
    __tablename__ = "summarize_settings"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    text = Column(String)
    link = Column(String)
