# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, DateTime

from app import db, login_manager
import bcrypt

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    salt = Column(String(255), nullable=False, unique=True)
    password = Column(String(255))
    first_name = Column(String(150))
    last_name = Column(String(150))
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    remember_token = Column(String(255), unique=True)
    sector = Column(String(45))
    watchlist = Column(String(45))
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

        self.password = bcrypt.hashpw(self.password.encode(), self.salt.encode()).decode() 

    def get_id(self):
        return self.remember_token
    
    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(remember_token=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
