import pymysql
import config

db = cursor = None

class MPengembalian:
	def __init__ (self, id_pengembalian=None, nim=None, id_alat=None,  jumlah=None, tgl_kembali=None, kondisi=None, status_alat=None):
		self.id_pengembalian = id_pengembalian
		self.nim = nim
		self.id_alat = id_alat	
		self.jumlah = jumlah
		self.tgl_kembali = tgl_kembali
		self.kondisi = kondisi
		self.status_alat = status_alat
	
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
		cursor.execute("SELECT * FROM pengembalian")
		container = []
		for id_pengembalian,nim, id_alat,jumlah,tgl_kembali,kondisi,status_alat in cursor.fetchall():
			container.append((id_pengembalian,nim, id_alat,jumlah,tgl_kembali,kondisi,status_alat))
		self.closeDB()
		return container
		
	def getDBbyId_pengembalian(self, id_pengembalian):
		self.openDB()
		cursor.execute("SELECT * FROM pengembalian WHERE id_pengembalian='%s'" % id_pengembalian)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE pengembalian SET nim='%s', id_alat='%s', jumlah='%s', tgl_kembali='%s', kondisi='%s', status_alat='%s' WHERE id_pengembalian=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_pengembalian):
		self.openDB()
		cursor.execute("DELETE FROM peminjaman WHERE id_pengembalian=%s" % id_pengembalian)
		db.commit()
		self.closeDB()