# -*- coding:utf-8 -*-
import os, sys
from urlparse import urlparse
from lib.session import ItsdangerousSessionInterface

#flask
from flask import Flask, render_template, request, g


MODULES = ['home', 'auth', 'picto']

def pictobump_app(config):
	app = Flask(__name__, static_folder="assets")
	app.session_interface = ItsdangerousSessionInterface()

	configure_app(app, config)
	configure_database(app)
	configure_auth(app)
	configure_csrf(app)
	configure_controllers(app)
	configure_error_handlers(app)

	return app

def configure_app(app, config):
	app.config.from_object(config)
	app.config["APP_ROOT"] = os.path.dirname(os.path.realpath(__file__))

def configure_controllers(app, modules=None):
	cur = os.path.abspath(__file__)
	sys.path.append(os.path.dirname(cur) + '/controllers')
	for mod in ( MODULES or modules ):
		module = __import__('%s_controller' % mod)
		app.register_blueprint(getattr(module, mod))

def configure_database(app):
	from models import db
	app.config["DATABASE"] = {
		'name': os.path.join(app.config["APP_ROOT"], 'db/pictobump.db'),
		'engine': 'peewee.SqliteDatabase'
	}
	db.init_app(app)

def configure_auth(app):
	from lib.auth import Auth
	auth = Auth(app)

def configure_csrf(app):
	from lib.bgcsrf import Csrf
	csrf = Csrf(app)

def configure_error_handlers(app):
	#refer http://flask.pocoo.org/docs/patterns/errorpages/
    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        return render_template("errors/405.html", error=error), 405

    @app.errorhandler(500)
    def server_error_page(error):
    	print error
        return render_template("errors/500.html", error=error), 500
