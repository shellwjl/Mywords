# -*- coding: utf-8 -*-
from flask import render_template,abort,flash,request,jsonify
from .. import db
from ..models import User
# from ..email import send_email
from . import main
from .forms import NameForm,EditProfileForm
from flask.ext.login import login_required,current_user,redirect,url_for
from .. import shanbei


APP_KEY="6ad9b45dc12edbf03943"
APP_SECRET="137107a506558960555851be0a78c5e8860d86af"
CALLBACK_URL = 'http://127.0.0.1:5000/auth/Shanbeilogin'
client=shanbei.APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)

from lxml import etree
root = etree.parse('app/static/cet4.xml')
cet4words = root.xpath('//wordbook/item/word/text()')
root2 = etree.parse('app/static/cet6.xml')
cet6words = root2.xpath('//wordbook/item/word/text()')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/userInfo/<username>')
def userInfo(username):
    user=User.query.filter_by(username=username).first()
    acc = client.getAccount1(current_user.access_token)
    if user is None:
        abort(404)
    return  render_template('userInfo.html',user=user,avatar=acc['avatar'])

@main.route('/remWord')
@login_required
def remWord():
    if current_user.wordrange=="CET-4":
        return render_template('remWord.html',words=cet4words,level="CET-4",wordsnum=current_user.everyrange);
    else:
        return render_template('remWord.html',words=cet6words,level="CET-6",wordsnum=current_user.everyrange);

@main.route('/wordexp')
@login_required
def wordexp():
    word=request.args.get('a',type=str)
    wordexps=client.getWordExp(word)
    access_token=current_user.access_token
    wordsentence=client.getSentences(wordexps['data']['id'],access_token)
    notes=client.getNotes(wordexps['data']['id'],access_token)
    Synonyms=client.getSynonyms(word)
    return jsonify(result1=wordexps['data']['definition'],notes=notes['data'][0]['content'],
                   wordsentence=wordsentence['data'][0]['annotation'],synonyms=Synonyms)




@main.route('/addnotes')
@login_required
def addwords():
    access_token=current_user.access_token
    word=request.args.get('word',type=str)
    print(word)
    usernotes=request.args.get('wordnotes',type=str)
    print(usernotes)
    wordexps=client.getWordExp(word)
    usernotes=client.addnotes(wordexps['data']['id'],usernotes=usernotes,access_token=access_token)
    return jsonify(usernotes=usernotes['data']['content'])

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.wordrange=form.language.data
        current_user.everyrange=form.everyrange.data
        db.session.add(current_user)
        flash(u'更新成功')
        return redirect(url_for('.userInfo',username=current_user.username))
    form.name.data=current_user.username
    form.location.data=current_user.location
    form.language.data=current_user.wordrange
    form.everyrange.data=current_user.everyrange
    return render_template('edit_profile.html',form=form)