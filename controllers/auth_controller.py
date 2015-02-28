# -*- coding:utf-8 -*-
import requests

from datetime import datetime
from flask import Blueprint, request, render_template, session, flash, abort, url_for, redirect, g

from lib.auth import logout_auth
from lib.oauth2 import OAuth2
from conf.settings import Dev
from models.users import Users

auth =  Blueprint('auth', __name__)

fbOAuth2 = OAuth2(Dev.FACEBOOK_APP_ID, Dev.FACEBOOK_APP_SECRET,
				site='https://www.facebook.com',
				authorization_url='/dialog/oauth',
				token_url='/oauth/access_token')

def _getFacebookUserInfo(code):
	resp = None
	fbOAuth2.site = "https://graph.facebook.com"
	fbresp = fbOAuth2.get_token(code, grant_type='authorization_code')
	access_token = fbresp.get("access_token", None)
	if access_token:
		remote_params = {'access_token' : access_token}
		fr = requests.get('https://graph.facebook.com/me', params=remote_params, timeout=60)
		if fr.status_code == requests.codes.ok:
			resp = fr.json()
			resp['access_token'] = access_token

	return resp

def signin():
	return render_template("auth/signin.html")

def signout():
	logout_auth()
	return redirect(url_for('auth.signin'))

def social_authorized(provider='facebook'):
	if request.args.get('code', None):
		oAuthUserInfo = None
		if (provider.lower() in 'facebook'):
			oAuthUserInfo = _getFacebookUserInfo(request.args.get('code'))
		else:
			flash('Not supported login provider')
			return redirect(url_for('auth.signin'))
		#print oAuthUserInfo
		if oAuthUserInfo:
			emailId = oAuthUserInfo.get('email', None)
			user = Users.getUserByEmailId(emailid=emailId)
			if not user:
				user = Users(emailid=emailId)
				user.name = oAuthUserInfo.get('name', None)
				user.fbid = oAuthUserInfo.get('id', None)
				user.access_token = oAuthUserInfo.get('access_token')[0]
				user.created_at = datetime.utcnow()
				user.save()
				if user.userid:
					session["emailid"] = user.emailid
					g.auth = user
				else:
					flash('Failed to save user information', 'error')
			else:
				session["emailid"] = user.emailid
				g.auth = user
		else:
			flash('Failed to get user information', 'error')
	elif request.args.get('error', None):
		flash(u'What happened?')
	else:
		flash(u'What happened?')

	return redirect(url_for('home.index'))

def social_login(provider=''):
	if provider.lower() in 'facebook':
		redirect_uri = url_for('auth.social_authorized', provider='facebook', _external=True)
		fbOAuth2.site = "https://www.facebook.com"
		auth_url = fbOAuth2.authorize_url(callback=redirect_uri,
										 scope='email',
										 response_type='code')
		return redirect(auth_url)
	return render_template("auth/signin.html")

auth.add_url_rule('/signout', 'signout', signout, methods=['GET'])
auth.add_url_rule('/signin', 'signin', signin, methods=['GET'])
auth.add_url_rule('/auth/<path:provider>', 'social_login', social_login, methods=['POST'])
#TODO:change the url
auth.add_url_rule('/auth/authorized/<path:provider>', 'social_authorized', social_authorized, methods=['GET'])