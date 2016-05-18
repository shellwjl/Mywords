# -*- coding: utf-8 -*-
__author__ = 'wjl'

from flask import redirect, request, url_for, flash
from . import auth
from flask.ext.login import logout_user, login_required,login_user
from .. import shanbei
from .. import db
from ..models import User

APP_KEY="6ad9b45dc12edbf03943"
APP_SECRET="137107a506558960555851be0a78c5e8860d86af"
CALLBACK_URL = 'http://127.0.0.1:5000/auth/Shanbeilogin'
client=shanbei.APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)


@auth.route('/login')
def login():
    login_url = client.get_authorize_url(redirect_uri=CALLBACK_URL)
    return redirect(login_url)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

#api授权后的回调地址
@auth.route('/Shanbeilogin',methods=['GET', 'POST'])
def shanbeiLogin():
    code=request.args.get('code')
    r=client.request_access_token(str(code))
    client.set_access_token(r.access_token, r.expires_in)
    acc = client.getAccount()
    user = User.query.filter_by(username=acc['username']).first()
    if user is None:
        user = User(username=acc['username'],access_token=r.access_token)
        db.session.add(user)
        db.session.commit()
    else:
        pass
    login_user(user)
    return redirect(request.args.get('next') or url_for('main.edit_profile'))


