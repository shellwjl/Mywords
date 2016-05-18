# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,SelectField,IntegerField
from wtforms.validators import DataRequired,Length


class NameForm(Form):
    name=StringField(u'你的名字？',validators=[DataRequired()])
    submit=SubmitField(u'提交')

class EditProfileForm(Form):
    name=StringField(u'用户名',validators=[Length(0,64)])
    location=StringField(u'来自于',validators=[Length(0,64)])
    everyrange=SelectField(u'每日单词量',choices=[('50', '50'), ('100', '100'), ('150', '150')],validators=[DataRequired()],default='100')
    language=SelectField(u'词汇范围', choices=[('CET-4', 'CET-4'), ('CET-6', 'CET-6')],default='CET-4')
    submit=SubmitField(u'确认')
