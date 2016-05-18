# -*- coding: utf-8 -*-
__author__ = 'wjl'
from . import db,login_manager
from flask.ext.login import UserMixin




class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    access_token=db.Column(db.String(64))
    location=db.Column(db.String(64))
    wordrange=db.Column(db.String(64))
    everyrange=db.Column(db.String(64),default='50')

    def __repr__(self):
        return '<User %r>' % self.username

#Flask-Login 要实现一个回调函数,使用指定的标识符加载用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

