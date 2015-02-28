# -*- coding:utf-8 -*-
import requests

from datetime import datetime

from flask import Blueprint, request, render_template, flash, abort, url_for, redirect, g

from lib.auth import login_required
from models.users import Users
from models.pictos import Pictos

home =  Blueprint('home', __name__)

def index():
	if g.auth:
		pictos = Pictos.getPictosByUserId(g.auth.fbid)
		pictoinvite = Pictos.getPictoInvitesByFbId(g.auth.fbid)
		return render_template("home/index.html", pictoList = pictos, inviteList = pictoinvite)
	else:
		return redirect(url_for('auth.signin'))

def invite():
	page = int(request.args.get('page', 1))
	remote_params = {'access_token' : g.auth.access_token, 'limit' : 50, 'offset':((page-1) * 50)}
	resp = requests.get('https://graph.facebook.com/me/friends', params=remote_params)
	if resp.status_code == requests.codes.ok:
		frnds = resp.json()
		return render_template("home/invite.html", frndsList = frnds.get('data', None), page=page)
	return redirect(url_for('home.index'))

def add_invite(friendid=None):
	if friendid:
		remote_params = {'access_token' : g.auth.access_token}
		resp = requests.get(('https://graph.facebook.com/%s' % friendid), params=remote_params)
		if resp.status_code == requests.codes.ok:
			frnd = resp.json()
		picto = Pictos(userid=g.auth.fbid)
		picto.username = g.auth.name
		picto.frndid = friendid
		picto.frndname = frnd.get('name', None)
		picto.created_at = datetime.utcnow()
		picto.save()
		return redirect(url_for('picto.index',pictoid=picto.pictoid))
	return redirect(url_for('home.invite'))

home.add_url_rule('/', 'index', index, methods=['GET'])
home.add_url_rule('/invite/<path:friendid>', 'add_invite', login_required(add_invite), methods=['GET'])
home.add_url_rule('/invite/', 'invite', login_required(invite), methods=['GET'])