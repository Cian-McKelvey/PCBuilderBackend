from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine, select, Boolean
from sqlalchemy.orm import Session
from constants import RELATIONAL_DATABASE_URL, RELATIONAL_TABLE_NAME

"""DO NOT RUN IN FILE - RUN FROM ROOT"""

metadata_obj = MetaData()  # Object that holds the metadata for each of the tables in the database
user_table = Table(
    RELATIONAL_TABLE_NAME,  # Specifies the name of the table
    metadata_obj,  # The metadata object
    # Creates columns for id, name, fullname - provides a primary key and the datatypes
    Column("id", Integer, primary_key=True),  # Primary key is here
    Column("firstname", String(30)),
    Column("surname", String(30)),
    Column("username", String(30)),
    Column("email", String(30)),
    Column("password", String(20)),
    Column("admin", Boolean, default=False),
)

engine = create_engine(RELATIONAL_DATABASE_URL, echo=True)

# Create a connection from the engine
connection = engine.connect()

# Create a session
session = Session(engine)

# Check if the table already exists
if not connection.dialect.has_table(connection, RELATIONAL_TABLE_NAME):
    # If the table doesn't exist, create it
    metadata_obj.create_all(engine)

# Reflect the existing database schema
metadata_obj.reflect(engine)

# Print table details
for table in metadata_obj.tables.values():
    print(f"Table: {table.name}")
    for column in table.columns:
        print(f"  Column: {column.name}, Type: {column.type}")
    print()

# Close the connection
connection.close()
session.close()
