from sqlalchemy import select
from sqlalchemy.orm import Session
from orm_setup import engine
from pc_builder_backend.build_tables import user_table
from user import User
from user_database_methods import add_new_user, delete_user, update_user_password

session = Session(engine)

# cian = User(
#     firstname="Cian",
#     surname="McKelvey",
#     username="cianbro",
#     email="cian@gmail.com",
#     password="example_password"
# )
#
# session.add(cian)  # Adds the cian obj up to be added to the database in a temporary state
# session.flush()  # Adds the new changes in the session object to the database
# session.commit()  # Commits these changes

# Modify the SELECT query to include the ID
select_query = select(user_table)
# Execute the query and fetch all results
result = session.execute(select_query).fetchall()

# Print the entire contents of the Users table
print("\nContents of Users table:")
for row in result:
    print(row)


add_result = add_new_user(user_session=session, first_name="Cian", last_name="McKelvey",
                          username="McKelvey-Cian", email="cian.p.mckelvey@gmail.com", password="Password123")

if add_result:
    print("\nSuccessfully added new user\n")
else:
    print("Failed to add new user")


# Modify the SELECT query to include the ID
select_query = select(user_table)
# Execute the query and fetch all results
result = session.execute(select_query).fetchall()

# Print the entire contents of the Users table
print("\nContents of Users table:")
for row in result:
    print(row)

update_result = update_user_password(user_session=session, username="McKelvey-Cian",
                                     old_password="Password123", new_password="Pass")

if update_result:
    print("\nUpdated password successfully\n")

# Modify the SELECT query to include the ID
select_query = select(user_table)
# Execute the query and fetch all results
result = session.execute(select_query).fetchall()

# Print the entire contents of the Users table
print("\nContents of Users table:")
for row in result:
    print(row)


delete_result = delete_user(user_session=session, username="McKelvey-Cian", password="Pass")

if delete_result:
    print("\nDeleted user successfully\n")

# Modify the SELECT query to include the ID
select_query = select(user_table)
# Execute the query and fetch all results
result = session.execute(select_query).fetchall()

# Print the entire contents of the Users table
print("\nContents of Users table:")
for row in result:
    print(row)

session.close()
