from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    handle: str
    token: str | None = None
    user_id: int | None = None
