from flask_wtf import Form
from wtforms import FileField, SubmitField
from datetime import datetime
import pymysql
import config

class MSimpanUser:
	def __init__ (self, id_user=None, level=None, nama=None, username=None, password=None, jenis_kelamin=None):
		self.id_user = id_user
		self.level = level
		self.nama = nama
		self.username = username
		self.password = password
		self.jenis_kelamin = jenis_kelamin

	def openDB (self):
		global db, cursor
		db = pymysql.connect(
			config.DB_HOST,
			config.DB_USER,
			config.DB_PASSWORD,
			config.DB_NAME)
		cursor = db.cursor()

	def closeDB(self):
		global db, cursor
		db.close()

	def selectDB(self):
		self.openDB()
		cursor.execute("SELECT * FROM pengguna")
		container = []
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO pengguna (id_user, level, nama, username, password, jenis_kelamin) VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % data)
		db.commit()
		self.closeDB()

	def getuserDB(self, username):
		self.openDB()
		cursor.execute("SELECT * FROM pengguna where $_SESSION['username']=$username" % username)
		db.commit()
		self.closeDB()

