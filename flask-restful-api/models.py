# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# import datetime

from __init__ import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    cdsid = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(50))
    user_type = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(60))
    description = db.Column(db.String(255))

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(30))
    status = db.Column(db.String(20))
    description = db.Column(db.String(255))
    resource_type = db.Column(db.String(20))
    # pub_time = db.Column(db.DateTime)
    # update_time = db.Column(db.DateTime)

    # def save_resource(self, *args, **kwargs):
    #     now = datetime.datetime.now()
    #     if not self.pub_time:
    #         self.pub_time = now
    #     self.update_time = now

    #     return super(Resource, self).save_resouce(*args, **kwargs)
