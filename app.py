from flask import Flask, render_template, jsonify, json, session, \
request, redirect, url_for
from models_alat import MAlat_lab
from models_jadwal import MJadwal_praktikum
from models_peminjaman import MPeminjaman
from models_pengembalian import MPengembalian
from models_buat_akun import MSimpanUser
from models_user import Pengguna
from datetime import datetime
import pymysql
import time
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = '1234567890!@#$%^&*()'
application.config['MAX_CONTENT_PATH'] = 10000000

#<--------------------------------------------LOGIN--------------------------------------->
@application.route('/')
def index():
	if 'username' in session and session['level'] == 'petugas':
		username = session['username']
		level = session['level']
		id_user = session['id_user']
		models = Pengguna()
		nama = models.selectnama(id_user)
		return render_template('data_alat_lab.html', username = username, level=level, id_user=id_user, nama=nama)
	elif 'username' in session and session['level'] == 'dosen':
		username = session['username']
		level = session['level']
		id_user = session['id_user']
		models = Pengguna()
		nama = models.selectnama(id_user)
		return render_template('jadwal_praktikum_dosen.html', username = username, level=level, id_user=id_user, nama=nama)
	elif 'username' in session and session['level'] == 'mahasiswa':
		username = session['username']
		level = session['level']
		id_user = session['id_user']
		models = Pengguna()
		nama = models.selectnama(id_user)
		return render_template('jadwal_praktikum_mahasiswa.html', username = username, level=level, id_user=id_user, nama=nama)
	return redirect(url_for('login'))

@application.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pengguna = Pengguna(username, password)
        if pengguna.authenticate():
            session['username'] = username
            session['id_user'] = pengguna.getId()
            session['level'] = pengguna.accountType()
            return redirect(url_for('index'))
        msg = 'Salah!'
        return render_template('login.html', msg = msg)
    return render_template('login.html')

@application.route('/buat_akun', methods = ['GET', 'POST'])
def buat_akun():
	if request.method == 'POST':
		id_user = request.form['id_user']
		level = request.form['level']
		username = request.form['username']
		password = request.form['password']
		nama = request.form['nama']
		jenis_kelamin = request.form['jenis_kelamin']
		data = (id_user, level, nama, username, password,jenis_kelamin)
		models = MSimpanUser()
		models.insertDB(data)
		return redirect(url_for('login'))
	else:
		return render_template('buat_akun.html')

@application.route('/logout')
def logout():
    session.pop('username', '')
    return redirect(url_for('index'))

#<--------------------------------------------DATA ALAT LAB--------------------------------------->
@application.route('/data_alat_lab')
def data_alat_lab():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MAlat_lab()
	container = []
	container = models.selectDB()
	return render_template('data_alat_lab.html',container=container, id_user=id_user, nama=nama)

@application.route('/insert_alat_lab', methods=['GET', 'POST'])
def insert_alat_lab():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	if request.method == 'POST':
		nama_alat = request.form['nama_alat']
		jumlah = request.form['jumlah']
		kondisi = request.form['kondisi']
		keterangan = request.form['keterangan']
		data = (nama_alat, jumlah, kondisi, keterangan)
		models = MAlat_lab()
		models.insertDB(data)
		return redirect(url_for('data_alat_lab'))
	else:
		return render_template('insert_alat_lab.html', id_user=id_user, nama=nama)

@application.route('/update_alat_lab/<id_alat>')
def update_alat_lab(id_alat):
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MAlat_lab()
	data = models.getDBbyId_alat(id_alat)
	return render_template('update_alat_lab.html', data= data, id_user=id_user)

@application.route('/update_prosess', methods=['GET', 'POST'])
def update_prosess():
	id_alat = request.form['id_alat']
	nama_alat = request.form['nama_alat']
	jumlah = request.form['jumlah']
	kondisi = request.form['kondisi']
	keterangan = request.form['keterangan']
	data = (nama_alat, jumlah, kondisi, keterangan, id_alat)
	models = MAlat_lab()
	models.updateDB(data)
	return redirect(url_for('data_alat_lab'))

@application.route('/delete_alat_lab/<id_alat>')
def delete_alat_lab(id_alat):
	models = MAlat_lab()
	models.deleteDB(id_alat)
	return redirect(url_for('data_alat_lab'))

#<--------------------------------------------DATA JADWAL PRAKTIKUM--------------------------------------->
@application.route('/jadwal_praktikum_petugas')
def jadwal_praktikum_petugas():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MJadwal_praktikum()
	container = []
	container = models.selectDB()
	return render_template('jadwal_praktikum_petugas.html',container=container, id_user=id_user, nama=nama)

@application.route('/jadwal_praktikum_dosen')
def jadwal_praktikum_dosen():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MJadwal_praktikum()
	container = []
	container = models.selectDB()
	return render_template('jadwal_praktikum_dosen.html',container=container, id_user=id_user, nama=nama)

@application.route('/jadwal_praktikum_mahasiswa')
def jadwal_praktikum_mahasiswa():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MJadwal_praktikum()
	container = []
	container = models.selectDB()
	return render_template('jadwal_praktikum_mahasiswa.html',container=container, id_user=id_user, nama=nama)

@application.route('/insert_jadwal_praktikum', methods=['GET', 'POST'])
def insert_jadwal_praktikum():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	if request.method == 'POST':
		id_ruang = request.form['id_ruang']
		tanggal_jadwal = request.form['tanggal_jadwal']
		jam = request.form['jam']
		data = (id_ruang, tanggal_jadwal, jam)
		models = MJadwal_praktikum()
		models.insertDB(data)
		return redirect(url_for('jadwal_praktikum_petugas'))
	else:
		return render_template('insert_jadwal_praktikum.html', id_user=id_user, nama=nama)

@application.route('/update_jadwal/<id_jadwal>')
def update_jadwal(id_jadwal):
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MJadwal_praktikum()
	data = models.getDBbyId_alat(id_jadwal)
	return render_template('update_jadwal_praktikum.html', data= data, id_user=id_user, nama=nama)

@application.route('/update_prosess_jadwal', methods=['GET', 'POST'])
def update_prosess_jadwal():
	id_ruang = request.form['id_ruang']
	id_jadwal = request.form['id_jadwal']
	tanggal_jadwal = request.form['tanggal_jadwal']
	jam = request.form['jam']
	data = (id_ruang, tanggal_jadwal, jam, id_jadwal)
	models = MJadwal_praktikum()
	models.updateDB(data)
	return redirect(url_for('jadwal_praktikum_petugas'))

@application.route('/delete_jadwal/<id_jadwal>')
def delete_jadwal(id_jadwal):
	models = MJadwal_praktikum()
	models.deleteDB(id_jadwal)
	return redirect(url_for('jadwal_praktikum_petugas'))

#<--------------------------------------------DATA PEMINJAMAN PETUGAS--------------------------------------->
@application.route('/petugas_peminjaman_dosen')
def petugas_peminjaman_dosen():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectpeminjaman_dosenDB()
	return render_template('petugas_peminjaman_dosen.html',container=container, id_user=id_user, nama=nama)

@application.route('/petugas_peminjaman_mahasiswa')
def petugas_peminjaman_mahasiswa():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectpeminjaman_mahasiswaDB()
	return render_template('petugas_peminjaman_mahasiswa.html',container=container, id_user=id_user, nama=nama)

#<--------------------------------------------DATA PEMINJAMAN DOSEN --------------------------------------->
@application.route('/peminjaman_dosen')
def peminjaman_dosen():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectDB(id_user)
	return render_template('peminjaman_dosen.html',container=container, id_user=id_user, nama=nama)

@application.route('/insert_peminjaman_dosen', methods=['GET', 'POST'])
def insert_peminjaman_dosen():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	if request.method == 'POST':
		id_user = session.get('id_user')
		id_alat = request.form['id_alat']
		jumlah = request.form['jumlah']
		tgl_peminjaman = request.form['tgl_peminjaman']
		tgl_pengembalian = request.form['tgl_pengembalian']
		keterangan = request.form['keterangan']
		status = request.form['status']
		data = (id_user,id_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan, status)
		models = MPeminjaman()
		models.insertDB(data)
		return redirect(url_for('peminjaman_dosen'))
	else:
		return render_template('insert_peminjaman_dosen.html', id_user=id_user, nama=nama)

@application.route('/update_peminjaman_dosen/<id_peminjaman>')
def update_peminjaman_dosen(id_peminjaman):
	models = MPeminjaman()
	data = models.getDBbyId_peminjaman(id_peminjaman)
	return render_template('update_peminjaman_dosen.html', data= data)

@application.route('/update_prosess_peminjaman_dosen', methods=['GET', 'POST'])
def update_prosess_peminjaman_dosen():
	id_peminjaman = request.form['id_peminjaman']
	id_alat = request.form['id_alat']
	jumlah = request.form['jumlah']
	tgl_peminjaman = request.form['tgl_peminjaman']
	tgl_pengembalian = request.form['tgl_pengembalian']
	keterangan = request.form['keterangan']
	status = request.form['status']
	data = (id_alat, jumlah, tgl_peminjaman, tgl_pengembalian, keterangan, status,id_peminjaman)
	models = MPeminjaman()
	models.updateDB(data)
	return redirect(url_for('petugas_peminjaman_dosen'))

@application.route('/delete_peminjaman_dosen/<id_peminjaman>')
def delete_peminjaman_dosen(id_peminjaman):
	models = MPeminjaman()
	models.deleteDB(id_peminjaman)
	return redirect(url_for('petugas_peminjaman_dosen'))

#<--------------------------------------------DATA PEMINJAMAN MAHASISWA --------------------------------------->
@application.route('/peminjaman_mahasiswa')
def peminjaman_mahasiswa():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectDB(id_user)
	return render_template('peminjaman_mahasiswa.html',container=container, id_user=id_user, nama=nama)

@application.route('/insert_peminjaman_mahasiswa', methods=['GET', 'POST'])
def insert_peminjaman_mahasiswa():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	if request.method == 'POST':
		id_user = session.get('id_user')
		id_alat = request.form['id_alat']
		jumlah = request.form['jumlah']
		tgl_peminjaman = request.form['tgl_peminjaman']
		tgl_pengembalian = request.form['tgl_pengembalian']
		keterangan = request.form['keterangan']
		status = request.form['status']
		data = (id_user,id_alat,jumlah,tgl_peminjaman,tgl_pengembalian,keterangan,status)
		models = MPeminjaman()
		models.insertDB(data)
		return redirect(url_for('peminjaman_mahasiswa'))
	else:
		return render_template('insert_peminjaman_mahasiswa.html', id_user=id_user, nama=nama)

@application.route('/update_peminjaman_mahasiswa/<id_peminjaman>')
def update_peminjaman_mahasiswa(id_peminjaman):
	models = MPeminjaman()
	data = models.getDBbyId_peminjaman(id_peminjaman)
	return render_template('update_peminjaman_mahasiswa.html', data= data)

@application.route('/update_prosess_peminjaman_mahasiswa', methods=['GET', 'POST'])
def update_prosess_peminjaman_mahasiswa():
	id_peminjaman = request.form['id_peminjaman']
	id_alat = request.form['id_alat']
	jumlah = request.form['jumlah']
	tgl_peminjaman = request.form['tgl_peminjaman']
	tgl_pengembalian = request.form['tgl_pengembalian']
	keterangan = request.form['keterangan']
	status = request.form['status']
	data = (id_alat, jumlah, tgl_peminjaman, tgl_pengembalian, keterangan, status, id_peminjaman)
	models = MPeminjaman()
	models.updateDB(data)
	return redirect(url_for('petugas_peminjaman_mahasiswa'))

@application.route('/delete_peminjaman_mahasiswa/<id_peminjaman>')
def delete_peminjaman_mahasiswa(id_peminjaman):
	models = MPeminjaman()
	models.deleteDB(id_peminjaman)
	return redirect(url_for('petugas_peminjaman_mahasiswa'))

#<--------------------------------------------DATA PENGEMBALIAN PETUGAS--------------------------------------->
@application.route('/data_pengembalian_petugas')
def data_pengembalian_petugas():
	models = MPengembalian()
	container = []
	container = models.selectDB()
	return render_template('pengembalian_petugas.html',container=container)

#<--------------------------------------------DATA PENGEMBALIAN DOSEN--------------------------------------->
'''@application.route('/pengembalian_dosen')
def pengembalian_dosen():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectdikembalikan_dosenDB()
	return render_template('pengembalian_dosen.html',container=container, id_user=id_user, nama=nama)

#<--------------------------------------------DATA PENGEMBALIAN MAHASISWA--------------------------------------->
@application.route('/pengembalian_mahasiswa')
def pengembalian_mahasiswa():
	id_user = session['id_user']
	models = Pengguna()
	nama = models.selectnama(id_user)
	models = MPeminjaman()
	container = []
	container = models.selectdikembalikan_mahasiswaDB()
	return render_template('pengembalian_mahasiswa.html',container=container, id_user=id_user, nama=nama)

@application.route('/update_pengembalian/<id_pengembalian>')
def update_pengembalian(id_pengembalian):
	models = MPengembalian()
	data = models.getDBbyId_pengembalian(id_pengembalian)
	return render_template('update_pengembalian.html', data= data)

@application.route('/update_prosess_pengembalian', methods=['GET', 'POST'])
def update_prosess_pengembalian():
	nim = request.form['nim']
	id_alat = request.form['id_alat']
	jumlah = request.form['jumlah']
	tgl_kembali = request.form['tgl_kembali']
	kondisi = request.form['kondisi']
	status_alat = request.form['status_alat']
	data = (nim, id_alat, jumlah, tgl_kembali, kondisi, status_alat, id_pengembalian)
	models = MPengembalian()
	models.updateDB(data)
	return redirect(url_for('data_pengembalian_petugas'))

@application.route('/delete_alat_lab/<id_pengembalian>')
def delete_pengembalian(id_pengembalian):
	models = MPengembalian()
	models.deleteDB(id_pengembalian)
	return redirect(url_for('data_pengembalian_petugas'))'''

#<--------------------------------------------DATA PENGGUNA--------------------------------------->
@application.route('/pengguna')
def pengguna():
	models = Pengguna()
	container = []
	container = models.selectDB()
	return render_template('pengguna.html',container=container)

#<--------------------------------------------GRAFIK ALAT LAB--------------------------------------->
@application.route('/grafik')
def grafik():
	models = Pengguna()
	data_pengguna = models.selectjumlahpengguna()
	models = MAlat_lab()
	data_alat = models.selectjumlahalat()
	data_alat_lab = models.grafikjumlahalat()
	models = MPeminjaman()
	data_peminjaman = models.selectjumlahpeminjaman()
	data_peminjaman_alat = models.grafikpeminjaman()
	id_alat = []
	jumlah = []
	id_peminjaman = []
	nama_alat = []
	for i in data_alat_lab:
		id_alat.append(i[0])
		jumlah.append(i[1])
	for i in data_peminjaman_alat:
		id_peminjaman.append(i[0])
		nama_alat.append(i[1])

	return render_template('dashboard_petugas.html', data_pengguna=data_pengguna, data_alat=data_alat, data_peminjaman=data_peminjaman, 
		data_alat_lab= json.dumps(data_alat_lab), id_alat= json.dumps(id_alat), jumlah= json.dumps(jumlah), data_peminjaman_alat=json.dumps(data_alat_lab), id_peminjaman=json.dumps(id_peminjaman), nama_alat=json.dumps(nama_alat))

'''@application.route('/cetak_data_survei', methods=['GET'])
def cetak_data_survei():
	if request.method=='GET':
		models = MAlat_lab()
		container = []
		container = models.selectDB()
		date_time = datetime.now()
		tanggal = date_time.strftime("%d %b %Y")
		return render_template('cetak_data_survei.html', container=container, tanggal=tanggal)'''

if __name__ == '__main__':
	application.run(debug=True)