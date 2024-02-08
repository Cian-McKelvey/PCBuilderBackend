import uuid
import datetime

from orm_setup import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from constants import RELATIONAL_TABLE_NAME


class User:
    def __init__(self, first_name, last_name, username, email, password):
        self.user_id = str(uuid.uuid1())  # Generates a user id on initialisation
        self.firstname = first_name
        self.surname = last_name
        self.username = username
        self.email = email
        self.password = password  # Password will be hashed before creating an instance
        self.admin = False
        self.registration_date = datetime.datetime.now()  # Registers when the user created an account

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.firstname,
            "last_name": self.surname,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "admin": self.admin,
            "registration_date": self.registration_date
        }

    def __repr__(self):
        return f"User: Name={self.firstname} {self.surname}  username={self.username}  email={self.email}"


"""
    Below is the ORM mapped class in case there is time to return to a RDBMS
"""


# class User(Base):
#
#     __tablename__ = RELATIONAL_TABLE_NAME
#
#     # Creates an id column of type int and is the primary key, mapped_column sets it to a column in the db
#     id: Mapped[int] = mapped_column(primary_key=True)
#
#     # Creates a firstname field of type string, must be not null
#     firstname: Mapped[str] = mapped_column(String(30), nullable=False)
#
#     # Creates a surname field of type string, must be not null
#     surname: Mapped[str] = mapped_column(String(30), nullable=False)
#
#     # Username is a string that must be unique and not null
#     username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
#
#     # Email is a string that must be unique and not null
#     email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
#
#     # Password is a string that must be not null
#     password: Mapped[str] = mapped_column(String(20), nullable=False)
#
#     # Creates an admin field - sets default to false so new admin users cant be created this way
#     admin: Mapped[bool] = mapped_column(unique=False, default=False)
#
#     def __repr__(self):
#         return f"User: Name={self.firstname} {self.surname}  username={self.username}  email={self.email}"

