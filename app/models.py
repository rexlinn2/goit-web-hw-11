from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    birthday: Mapped[object] = mapped_column(Date, nullable=False, index=True)
    additional_data: Mapped[str | None] = mapped_column(Text, nullable=True)
