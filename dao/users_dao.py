from dao.models.users import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        """Get user by id"""
        return self.session.query(User).get(uid)

    def get_all(self):
        """Get all users"""
        return self.session.query(User).all()

    def create(self, user_date):
        """Create new user"""
        user = User(**user_date)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid):
        """delete user by id"""
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_date):
        """update user by id"""
        user = self.get_one(user_date.get("id"))
        # id наверное надо поменять на userid в строке выше
        user.userid = user_date.get("userid")
        user.username = user_date.get("username")
        user.first_name = user_date.get("first_name")
        user.last_name = user_date.get("last_name")
        # user.date_registration = user_date.get("date_registration")
        # думаю это не надо в строке выше

        self.session.add(user)
        self.session.commit()
