# -*- coding:utf-8 -*-
from peewee import *
from flask import g
from datetime import datetime
from models import db

class Pictos(db.Model):
	pictoid = PrimaryKeyField()
	userid = CharField()
	username = CharField()
	userscore = IntegerField(default=0)
	frndid = CharField()
	frndname = CharField()
	frndscore = IntegerField(default=0)
	created_at = DateTimeField(default=datetime.utcnow())

	class Meta:
		order_by = ('created_at',)

	@property
	def is_owner(self):
		return (self.userid == g.auth.fbid)

	@property
	def friendname(self):
		return self.frndname if self.is_owner else self.username
		
	@classmethod
	def getPictoById(cls, pictoid, fbid):
		retResult = None
		try:
			retResult = cls.get((Pictos.pictoid == pictoid) & (Pictos.userid == fbid) | (Pictos.frndid == fbid))
		except Exception, e:
			print "Picto doesnot exist"
		return retResult

	@classmethod
	def getPictosByUserId(cls, userid):
		retResult = None
		try:
			retResult = cls.select().where((Pictos.userid == userid))
		except Exception, e:
			print "Picto's doesnot exist"
		return retResult

	@classmethod
	def getPictoInvitesByFbId(cls, fbid):
		retResult = None
		try:
			retResult = cls.select().where((Pictos.frndid == fbid))
		except Exception, e:
			print "Picto's doesnot exist"
		return retResult


Pictos.create_table(True)