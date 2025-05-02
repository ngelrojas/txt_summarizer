from sqlalchemy import Column, Integer, String
from connections.cnx import Base


class SummarizeSettings(Base):
    __tablename__ = "summarize_settings"
    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    provider = Column(String)
    open_ai_key = Column(String)
