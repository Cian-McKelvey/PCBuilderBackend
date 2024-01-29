from sqlalchemy.orm import Session

from orm_setup import engine
from user import User

session = Session(engine)

# Prints the whole user list
data = session.query(User).all()
for item in data:
    print("\n")
    print(item)
    print(f"USER - ID={item.id}  Name={item.firstname} {item.surname}  username={item.username} \n")
