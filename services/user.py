from dao.users_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        """get user by id"""
        return self.dao.get_one(uid)

    def get_all(self):
        """get all users"""
        return self.dao.get_all()

    def create(self, user_data: dict):
        """create new user"""
        return self.dao.create(user_data)

    def update(self, user_data):
        """update user"""
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        """delete user"""
        self.dao.delete(uid)