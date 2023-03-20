import pymysql
import config

db = cursor = None

class MPeminjaman:
	def __init__ (self, id_peminjaman=None, id_user=None, id_alat=None,  jumlah=None, tgl_peminjaman=None, tgl_pengembalian=None, keterangan=None, status=None):
		self.id_peminjaman = id_peminjaman
		self.id_user = id_user
		self.id_alat = id_alat	
		self.jumlah = jumlah
		self.tgl_peminjaman = tgl_peminjaman
		self.tgl_pengembalian = tgl_pengembalian
		self.keterangan = keterangan
		self.status = status
	
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

	def selectDB(self, id_user):
		self.openDB()
		cursor.execute("SELECT p.id_peminjaman as no, u.nama, a.nama_alat, p.jumlah, p.tgl_peminjaman, p.tgl_pengembalian, p.keterangan, p.status\
			from peminjaman p, pengguna u, alat_lab a\
			where u.id_user=p.id_user and a.id_alat=p.id_alat and p.id_user=%s" % id_user)
		container = []
		for no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan, status))
		self.closeDB()
		return container

	def selectpeminjaman_dosenDB(self):
		self.openDB()
		cursor.execute("SELECT p.id_peminjaman as no, u.nama, a.nama_alat, p.jumlah, p.tgl_peminjaman, p.tgl_pengembalian, p.keterangan, p.status\
			from peminjaman p, pengguna u, alat_lab a\
			where u.id_user=p.id_user and a.id_alat=p.id_alat and level like '%dosen%'")
		container = []
		for no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan, status))
		self.closeDB()
		return container

	def selectpeminjaman_mahasiswaDB(self):
		self.openDB()
		cursor.execute("SELECT p.id_peminjaman as no, u.nama, a.nama_alat, p.jumlah, p.tgl_peminjaman, p.tgl_pengembalian, p.keterangan, p.status\
			from peminjaman p, pengguna u, alat_lab a\
			where u.id_user=p.id_user and a.id_alat=p.id_alat and level like '%mahasiswa%'")
		container = []
		for no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status))
		self.closeDB()
		return container

	def insertDB(self, data):
		self.openDB()
		cursor.execute("INSERT INTO peminjaman (id_user, id_alat, jumlah, tgl_peminjaman, tgl_pengembalian, keterangan, status) VALUES('%s','%s','%s','%s','%s','%s','%s')" % data)
		db.commit()
		self.closeDB()
		
	def getDBbyId_peminjaman(self, id_peminjaman):
		self.openDB()
		cursor.execute("SELECT * FROM peminjaman WHERE id_peminjaman='%s'" % id_peminjaman)
		data = cursor.fetchone()
		return data

	def updateDB(self, data):
		self.openDB()
		cursor.execute("UPDATE peminjaman SET id_alat='%s', jumlah='%s', tgl_peminjaman='%s', tgl_pengembalian='%s', keterangan='%s', status='%s' WHERE id_peminjaman=%s" % data)
		db.commit()
		self.closeDB()

	def deleteDB(self, id_peminjaman):
		self.openDB()
		cursor.execute("DELETE FROM peminjaman WHERE id_peminjaman=%s" % id_peminjaman)
		db.commit()
		self.closeDB()

	def selectjumlahpeminjaman(self):
		self.openDB()
		cursor.execute("SELECT count(id_peminjaman) FROM peminjaman")
		data_peminjaman = (cursor.fetchone())[0]
		return data_peminjaman

	def grafikpeminjaman(self):
		self.openDB()
		q= ("SELECT count(p.id_peminjaman), d.nama_alat from peminjaman p, alat_lab d WHERE p.id_alat=d.id_alat group by d.nama_alat")
		container = []
		cursor.execute(q)
		for id_peminjaman, nama_alat in cursor.fetchall():
			container.append((id_peminjaman,nama_alat))
		self.closeDB()
		return container

	def selectdipinjam_dosenDB(self):
		self.openDB()
		cursor.execute("SELECT p.id_peminjaman as no, u.nama, a.nama_alat, p.jumlah, p.tgl_pengembalian, p.keterangan as kondisi, p.status\
			from peminjaman p, pengguna u, alat_lab a\
			where p.id_user=u.id_user and p.id_alat=a.id_alat and level like '%dosen%' and status like '%dipinjam%'")
		container = []
		for no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan, status))
		self.closeDB()
		return container

	def selectdipinjam_dosenDB(self):
		self.openDB()
		cursor.execute("SELECT p.id_peminjaman as no, u.nama, a.nama_alat, p.jumlah, p.tgl_pengembalian, p.keterangan as kondisi, p.status\
			from peminjaman p, pengguna u, alat_lab a\
			where p.id_user=u.id_user and p.id_alat=a.id_alat and level like '%dosen%' and status='%dipinjam%'")
		container = []
		for no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan, status))
		self.closeDB()
		return container

	def selectdikembalikan_dosenDB(self):
		self.openDB()
		cursor.execute("SELECT * FROM dikembalikan_dosen")
		container = []
		for no,nama,nama_alat,jumlah,tgl_pengembalian,kondisi,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_pengembalian,kondisi, status))
		self.closeDB()
		return container

	def selectdikembalikan_mahasiswaDB(self):
		self.openDB()
		cursor.execute("SELECT * FROM dikembalikan_mahasiswa")
		container = []
		for no,nama,nama_alat,jumlah,tgl_pengembalian,kondisi,status in cursor.fetchall():
			container.append((no,nama,nama_alat,jumlah,tgl_pengembalian,kondisi, status))
		self.closeDB()
		return container