# -*- coding:utf-8 -*-
from peewee import *

from datetime import datetime
from models import db

class Users(db.Model):
	userid = PrimaryKeyField()
	emailid = CharField(unique=True)
	fbid = CharField()
	name = CharField()
	access_token = CharField()
	created_at = DateTimeField(default=datetime.utcnow())

	class Meta:
		order_by = ('created_at',)

	@classmethod
	def getUserByEmailId(cls, emailid):
		retResult = None
		try:
			retResult = cls.get((Users.emailid==emailid))
		except Exception, e:
			print "User doesnot exist"
			#raise e
		return retResult


Users.create_table(True)