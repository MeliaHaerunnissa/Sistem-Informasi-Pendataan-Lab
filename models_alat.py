import pymysql
import config

db = cursor = None

class MAlat_lab:
	def __init__ (self, id_alat=None, nama_alat=None, jumlah=None, kondisi=None, keterangan=None):
		self.id_alat = id_alat
		self.nama_alat = nama_alat
		self.jumlah = jumlah
		self.kondisi = kondisi
		self.keterangan = keterangan
	
	def openDB(self):
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
		cursor.execute("SELECT * FROM alat_lab")
		container = []
		for id_alat,nama_alat,jumlah,kondisi,keterangan in cursor.fetchall():
			container.append((id_alat,nama_alat,jumlah,kondisi,keterangan))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO alat_lab (nama_alat,jumlah,kondisi,keterangan) VALUES('%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def getDBbyId_alat(self, id_alat):
		self.openDB()
		cursor.execute("SELECT * FROM alat_lab WHERE id_alat='%s'" % id_alat)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE alat_lab SET nama_alat='%s', jumlah='%s', kondisi='%s', keterangan='%s' WHERE id_alat=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_alat):
		self.openDB()
		cursor.execute("DELETE FROM alat_lab WHERE id_alat=%s" % id_alat)
		db.commit()
		self.closeDB()

	def selectjumlahalat(self):
		self.openDB()
		cursor.execute("SELECT count(id_alat) FROM alat_lab")
		data_alat = (cursor.fetchone())[0]
		return data_alat

	def grafikjumlahalat(self):
		self.openDB()
		q= ("SELECT count(id_alat), jumlah from alat_lab")
		container = []
		cursor.execute(q)
		for id_alat, jumlah in cursor.fetchall():
			container.append((id_alat,jumlah))
			self.closeDB()
		return container