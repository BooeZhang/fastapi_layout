from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import sqlalchemy as sa

meta = sa.MetaData()


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_at: Mapped[datetime] = mapped_column(default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(default=datetime.now())
    metadata = meta

