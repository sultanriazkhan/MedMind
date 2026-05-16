from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, name):
        self.id = str(id)
        self.email = email
        self.name = name

    @staticmethod
    def get_by_id(user_id):
        if not user_id:
            return None

        return User(
            id=user_id,
            email="demo@healthai.com",
            name="Demo User"
        )

    @staticmethod
    def get_by_email(email):
        if not email:
            return None

        return User(
            id="1",
            email=email,
            name=email.split("@")[0].title()
        )