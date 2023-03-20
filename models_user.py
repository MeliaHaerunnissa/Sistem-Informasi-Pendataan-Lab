import pymysql
import config

db = cursor = None

class Pengguna():
    def __init__ (self, username=None, password=None):
        self.username = username
        self.password = password

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
        cursor.execute("SELECT * FROM pengguna")
        container = []
        for id_user, level, nama, username, password, jenis_kelamin in cursor.fetchall():
            container.append((id_user, level, nama, username, password, jenis_kelamin))
        self.closeDB()
        return container

    def authenticate(self):
        self.openDB()
        cursor.execute("SELECT COUNT(*) FROM pengguna WHERE username = '%s' And password = '%s'" % (self.username, self.password))
        count_account = (cursor.fetchone())[0]
        self.closeDB()
        return True if count_account > 0 else False

    def accountType(self):
        self.openDB()
        cursor.execute("SELECT * FROM pengguna WHERE username = '%s' AND password = '%s'" % (self.username, self.password))
        account = (cursor.fetchone())
        self.closeDB()
        if account[1] =='petugas':
            return 'petugas'
        elif account[1] == 'dosen':
            return 'dosen'
        elif account[1] == 'mahasiswa':
            return 'mahasiswa'

    def getId(self):
        self.openDB()
        cursor.execute("SELECT id_user FROM pengguna WHERE username = '%s' AND password = '%s' " % (self.username, self.password))
        data = cursor.fetchone()
        self.closeDB()
        return data[0]

    def selectnama(self, id_user):
        self.openDB()
        cursor.execute("SELECT nama FROM pengguna WHERE id_user=%s" % id_user)
        nama = (cursor.fetchone())[0]
        return nama

    def selectjumlahpengguna(self):
        self.openDB()
        cursor.execute("SELECT count(id_user) FROM pengguna")
        data_pengguna = (cursor.fetchone())[0]
        return data_pengguna