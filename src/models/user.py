import uuid

from flask import session
from src.common.database import Database
from datetime import datetime


class User(object):

    def __init__(self, email, password, user_name=None, user_id=None, _id=None,
                 algorithm_beaten_count=None, budget_remaining=700000):
        self.algorithm_beaten_count = algorithm_beaten_count
        self.budget_remaining = budget_remaining
        self.email = email
        self.password = password
        self.user_name = user_name
        self.user_id = user_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())

    def json(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password,
            "budget_remaining": self.budget_remaining,
            "algorithm_beaten_count": self.algorithm_beaten_count,
            "_id": self._id
        }

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one('users', {'username': username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def valid_login(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        print(email)
        user = cls.get_by_email(email)
        if user is None:
            new_user = User(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

