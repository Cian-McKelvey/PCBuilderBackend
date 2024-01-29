from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import Session
from logger_config.logger_config import create_logger

from user import User


logger = create_logger('Users.log')


# Hash Passwords here before entering the account
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


def valid_user_check(user_session: Session, username: str, password: str) -> int:
    try:
        # Attempts to fetch as user with the provided username
        fetched_user = user_session.query(User).filter(User.username == username).first()

        if fetched_user is not None:
            # If a user is found, compare its password with the provided password, true if it's a match, false otherwise
            if fetched_user.password == password:
                logger.info(f"Account found with matching credentials")
                return fetched_user.id
            else:
                logger.info(f"Account password is incorrect")
                return -0
        else:
            logger.info(f"No account found with username : {username}")
            return -0

    except NoResultFound as e:
        logger.error(f"No result found during user lookup: {e}")
        return -0

    except SQLAlchemyError as e:
        logger.error(f"Error during user lookup: {e}")
        return -0


