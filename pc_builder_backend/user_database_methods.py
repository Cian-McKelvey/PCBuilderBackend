from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session
from logger_config.logger_config import create_logger

from user import User


logger = create_logger('Users.log')


def add_new_user(user_session: Session, first_name: str, last_name: str,
                 username: str, email: str, password: str):
    new_user = User(
        firstname=first_name,
        surname=last_name,
        username=username,
        email=email,
        password=password
    )
    try:
        user_session.add(new_user)
        user_session.flush()  # Adds the new changes in the session object to the database
        user_session.commit()
        logger.info(f"New user added successfully: {new_user.username}")
        return True

    except SQLAlchemyError as e:
        logger.error(f"Could not add new user: {e}")
        user_session.rollback()  # Rollback changes in case of an error
        return False


def delete_user(user_session: Session, username: str, password: str):
    try:
        # Brackets originally surrounded the query if there's an issue look at putting them back
        fetched_user = (user_session.query(User).filter(User.username == username, User.password == password)
                        .first())

        if fetched_user is not None:
            user_session.delete(fetched_user)
            user_session.flush()
            user_session.commit()
            logger.info(f"User ({username}) deleted successfully")
            return True

    # Catches the event of nothing being returned from the query
    except NoResultFound as e:
        logger.error(f"No result found to delete: {e}")
        return False

    except SQLAlchemyError as e:
        logger.error(f"Error deleting user: {e}")
        user_session.rollback()  # Rollback changes in case of an error
        return False


def update_user_password(user_session: Session, username: str, old_password: str, new_password: str):
    try:

        fetched_user = user_session.query(User).filter(User.username == username,
                                                       User.password == old_password).first()

        if fetched_user is not None:
            # Update fetched_user password to new_password
            fetched_user.password = new_password
            user_session.flush()
            user_session.commit()

            logger.info(f"User password updated for account: {username}")
            return True

    # Catches the event of nothing being returned from the query
    except NoResultFound as e:
        logger.error(f"No result found to update password: {e}")
        return False

    except SQLAlchemyError as e:
        logger.error(f"Error fetching user for password update: {e}")
        user_session.rollback()  # Rollback changes in case of an error
        return False

# This needs fixed, the return type isn't as intended, but the thing might still work fine, just need testing
# Can also use the user_table instead while fetching then build an object out of the result

# def fetch_user_by_username(user_session: Session, username: str) -> User:
#     try:
#         fetched_user = user_session.query(User).filter(User.username == username).first()
#
#         if fetched_user is not None:
#             return fetched_user
#
#     except NoResultFound as e:
#         logger.error(f"No result found during user lookup: {e}")
#
#     except SQLAlchemyError as e:
#         logger.error(f"Error during user lookup: {e}")
#
#     # If nothing is found, you may want to return None or raise an exception depending on your application logic.
#     return None
