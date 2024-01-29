from orm_setup import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from constants import RELATIONAL_TABLE_NAME


class User(Base):

    __tablename__ = RELATIONAL_TABLE_NAME

    # Creates an id column of type int and is the primary key, mapped_column sets it to a column in the db
    id: Mapped[int] = mapped_column(primary_key=True)

    # Creates a firstname field of type string, must be not null
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)

    # Creates a surname field of type string, must be not null
    surname: Mapped[str] = mapped_column(String(30), nullable=False)

    # Username is a string that must be unique and not null
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    # Email is a string that must be unique and not null
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    # Password is a string that must be not null
    password: Mapped[str] = mapped_column(String(20), nullable=False)

    # Creates an admin field - sets default to false so new admin users cant be created this way
    admin: Mapped[bool] = mapped_column(unique=False, default=False)

    def __repr__(self):
        return f"User: Name={self.firstname} {self.surname}  username={self.username}  email={self.email}"
