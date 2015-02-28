# -*- config:utf-8 -*-

from datetime import timedelta

import os

class Config(object):
    
    PRODUCT_NAME  = "Pictobump"
    INTERNAL_NAME = "pb"
    
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_NAME = "_%st" % INTERNAL_NAME
    SESSION_COOKIE_SECURE = True

    SECRET_KEY = '4c71424b7555624653476d314c7844636933744b54744c6e526f734453554d637154513863506a424175553d'
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

class Dev(Config):

	FACEBOOK_APP_ID = "268293243294103"
	FACEBOOK_APP_SECRET = "0c1b22beff83ae639ceb9e6fa3687caa"

	DEBUG = True

class Prod(Config):
    DEBUG = False
