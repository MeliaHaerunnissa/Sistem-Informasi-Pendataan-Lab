import pymysql
import config

db = cursor = None

class MJadwal_praktikum:
	def __init__ (self, id_ruang=None, id_jadwal=None, tanggal_jadwal=None, jam=None):
		self.id_ruang = id_ruang
		self.id_jadwal = id_jadwal
		self.tanggal_jadwal = tanggal_jadwal
		self.jam = jam
	
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
		cursor.execute("SELECT j.id_jadwal as no, r.nama_ruang, j.tanggal_jadwal, j.jam\
			from jadwal_praktikum j, ruang r\
			where r.id_ruang=j.id_ruang")
		container = []
		for no, nama_ruang, tanggal_jadwal, jam in cursor.fetchall():
			container.append((no, nama_ruang, tanggal_jadwal, jam))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO jadwal_praktikum (id_ruang, tanggal_jadwal, jam) VALUES('%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def getDBbyId_alat(self, id_jadwal):
		self.openDB()
		cursor.execute("SELECT * FROM jadwal_praktikum WHERE id_jadwal='%s'" % id_jadwal)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE jadwal_praktikum SET id_ruang='%s', tanggal_jadwal='%s', jam='%s' WHERE id_jadwal=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_jadwal):
		self.openDB()
		cursor.execute("DELETE FROM jadwal_praktikum WHERE id_jadwal=%s" % id_jadwal)
		db.commit()
		self.closeDB()

