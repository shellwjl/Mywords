# -*- coding: utf-8 -*-
__author__ = 'wjl'
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length

class ShanbeiLoginForm(Form):
    #预留头像等信息
    username=StringField(u'用户名',validators=[DataRequired()])
    submit=SubmitField(u'提交')

