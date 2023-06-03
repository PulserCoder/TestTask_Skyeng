from dao.users_dao import UserDAO
from services.user import UserService
from setup_db import session

user_dao = UserDAO(session=session)
user_service = UserService(user_dao)
