from sqlmodel import Field, Session, SQLModel, create_engine, select


class Summarize(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name_doc: str = Field(nullable=False)
    name_session: str = Field(nullable=False)
