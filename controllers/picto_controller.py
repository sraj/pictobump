# -*- coding:utf-8 -*-
import requests

from datetime import datetime

from flask import Blueprint, request, render_template, session, flash, abort, url_for, escape, redirect, current_app, g
from flask_peewee.utils import object_list

from lib.auth import login_required
from models.pictos import Pictos

picto =  Blueprint('picto', __name__)

def index(pictoid=None):
	if pictoid:
		picto = Pictos.getPictoById(pictoid, g.auth.fbid)
		if picto:
			return render_template('picto/picto.html', opicto = picto)
		else:
			flash(u'Requested Picto not exists..!!', 'error')
	return redirect(url_for('home.index'))


picto.add_url_rule('/picto/<path:pictoid>', 'index' ,login_required(index), methods=['GET'])