import sqlite3 # Import modul sqlite3 untuk menggunakan database
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk # Import modul Tkinter untuk membuat GUI   

# Fungsi untuk membuat databse dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') # ‘Conn’ berfungsi untuk membuat koneksi ke database ‘nilai_siswa.db’, jika tidak ada akan ter create
    cursor = conn.cursor() # ‘Cursor’ berfungsi untuk mengeksekusi perintah SQL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        ) 
    """) # ‘Cursor.execute’ berfungsi untuk mengeksekusi perintah SQL
    conn.commit() # ‘Conn.commit’ berfungsi untuk menyimpan perubahan ke database
    conn.close() # ‘Conn.close’ berfungsi untuk menutup koneksi ke database

# Memanggil fungsi untuk membuat database dan tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db') # ‘Conn’ berfungsi untuk membuat koneksi ke database ‘nilai_siswa.db’
    cursor = conn.cursor() # ‘Cursor’ berfungsi untuk mengeksekusi perintah SQL
    cursor.execute("SELECT * FROM nilai_siswa") # ‘Cursor.execute’ berfungsi untuk mengeksekusi perintah SQL
    rows = cursor.fetchall() # ‘Cursor.fetchall’ berfungsi untuk mengambil semua baris dari hasil query
    conn.close() # ‘Conn.close’ berfungsi untuk menutup koneksi ke database
    return rows

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db') # ‘Conn’ berfungsi untuk membuat koneksi ke database ‘nilai_siswa.db’
    cursor = conn.cursor() # ‘Cursor’ berfungsi untuk mengeksekusi perintah SQL
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi)) # ‘Cursor.execute’ berfungsi untuk mengeksekusi perintah SQL
    conn.commit() # ‘Conn.commit’ berfungsi untuk menyimpan perubahan ke database
    conn.close() # ‘Conn.close’ berfungsi untuk menutup koneksi ke database

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db') # ‘Conn’ berfungsi untuk membuat koneksi ke database ‘nilai_siswa.db’
    cursor = conn.cursor() # ‘Cursor’ berfungsi untuk mengeksekusi perintah SQL
    cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, biologi, fisika, inggris, prediksi, record_id)) # ‘Cursor.execute’ berfungsi untuk mengeksekusi perintah SQL
    conn.commit() # ‘Conn.commit’ berfungsi untuk menyimpan perubahan ke database
    conn.close() # ‘Conn.close’ berfungsi untuk menutup koneksi ke database 

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db') # ‘Conn’ berfungsi untuk membuat koneksi ke database ‘nilai_siswa.db’
    cursor = conn.cursor() # ‘Cursor’ berfungsi untuk mengeksekusi perintah SQL
    cursor.execute("DELETE FROM nilai_siswa WHERE id=?", (record_id,)) # ‘Cursor.execute’ berfungsi untuk mengeksekusi perintah SQL
    conn.commit() # ‘Conn.commit’ berfungsi untuk menyimpan perubahan ke database
    conn.close() # ‘Conn.close’ berfungsi untuk menutup koneksi ke database

# Fungsi untuk menghitung prediksi fakultas
def calculate_prediksi(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris: # Jika nilai biologi lebih besar dari fisika dan inggris, maka prediksi fakultas adalah Kedokteran
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris: # Jika nilai fisika lebih besar dari biologi dan inggris, maka prediksi fakultas adalah Teknik
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui" # Jika tidak ada nilai yang lebih besar, maka prediksi fakultas adalah Tidak Diketahui

# Fungsi untuk menangani tombol submit
def submit():
    try: 
        nama = nama_var.get() # Mengambil nilai dari input nama 
        biologi = int(biologi_var.get()) # Mengambil nilai dari input biologi dan mengonversi menjadi integer
        fisika = int(fisika_var.get()) # Mengambil nilai dari input fisika dan mengonversi menjadi integer
        inggris = int(inggris_var.get()) # Mengambil nilai dari input inggris dan mengonversi menjadi integer

        if not nama:
            raise Exception("Nama tidak boleh kosong") # Jika input nama kosong, maka akan menampilkan pesan error
        
        prediksi = calculate_prediksi(biologi, fisika, inggris) # Memanggil fungsi calculate_prediksi untuk menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi) # Memanggil fungsi save_to_database untuk menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") # Menampilkan pesan sukses
        clear_inputs() # Memanggil fungsi clear_inputs untuk mengosongkan input
        populate_table() # Memanggil fungsi populate_table untuk mengisi tabel dengan data baru
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}") # Menampilkan pesan error

# fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk diupdate") # Jika tidak ada data yang dipilih, maka akan menampilkan pesan error
        
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong") # Jika input nama kosong, maka akan menampilkan pesan error   
        
        prediksi = calculate_prediksi(biologi, fisika, inggris) # Memanggil fungsi calculate_prediksi untuk menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) # Memanggil fungsi update_database untuk memperbarui data di database

        messagebox.showinfo("Sukses", f"Data berhasil diperbarui!\nPrediksi Fakultas: {prediksi}") # Menampilkan pesan sukses
        clear_inputs() # Memanggil fungsi clear_inputs untuk mengosongkan input
        populate_table() # Memanggil fungsi populate_table untuk mengisi tabel dengan data baru
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")    

# fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus")
        
        record_id = int(selected_record_id.get())
        delete_database(record_id) # Memanggil fungsi delete_database untuk menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus") # Menampilkan pesan sukses
        clear_inputs() # Memanggil fungsi clear_inputs untuk mengosongkan input
        populate_table() # Memanggil fungsi populate_table untuk mengisi tabel dengan data baru
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}") # Menampilkan pesan error

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("") # Mengosongkan input nama
    biologi_var.set("") # Mengosongkan input biologi    
    fisika_var.set("") # Mengosongkan input fisika
    inggris_var.set("") # Mengosongkan input inggris
    selected_record_id.set("") # Mengosongkan input record id

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children(): # Menghapus semua baris yang ada di tabel
        tree.delete(row)    
    for row in fetch_data(): # Mengisi tabel dengan data dari database
        tree.insert("", "end", values=row)

# Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Mengambil item yang dipilih   
        selected_row = tree.item(selected_item)["values"] # Mengambil nilai dari item yang dipilih

        selected_record_id.set(selected_row[0]) # Mengisi input record id dengan nilai dari item yang dipilih   
        nama_var.set(selected_row[1]) # Mengisi input nama dengan nilai dari item yang dipilih
        biologi_var.set(selected_row[2]) # Mengisi input biologi dengan nilai dari item yang dipilih
        fisika_var.set(selected_row[3]) # Mengisi input fisika dengan nilai dari item yang dipilih
        inggris_var.set(selected_row[4]) # Mengisi input inggris dengan nilai dari item yang dipilih
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!") # Menampilkan pesan error   

# Inisialisasi database
create_database() # Memanggil fungsi create_database untuk membuat database dan tabel   

# Inisialisasi Tkinter
root = Tk() # Membuat jendela utama
root.title("Input Nilai Siswa") # Mengatur judul jendela
root.configure(bg="#DFF2EB") # Mengatur warna latar belakang jendela

# Variabel untuk input
nama_var = StringVar() # Variabel untuk input nama
biologi_var = StringVar() # Variabel untuk input biologi
fisika_var = StringVar() # Variabel untuk input fisika  
inggris_var = StringVar() # Variabel untuk input inggris
selected_record_id = StringVar() # Variabel untuk input record id

# Membuat label dan entry untuk input
Label(root, text="Nama Siswa", font=("Comic Sans MS", 12, "bold"), bg="#DFF2EB").grid(row=0, column=0, padx=10, pady=5, sticky='w') # Membuat label untuk input nama
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Membuat entry untuk input nama

Label(root, text="Biologi", font=("Comic Sans MS", 11, "bold"), bg="#DFF2EB").grid(row=1, column=0, padx=10, pady=5, sticky='w') # Membuat label untuk input biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Membuat entry untuk input biologi

Label(root, text="Fisika", font=("Comic Sans MS", 12, "bold"), bg="#DFF2EB").grid(row=2, column=0, padx=10, pady=5, sticky='w') # Membuat label untuk input fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Membuat entry untuk input fisika

Label(root, text="Inggris", font=("Comic Sans MS", 12, "bold"), bg="#DFF2EB").grid(row=3, column=0, padx=10, pady=5, sticky='w') # Membuat label untuk input inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Membuat entry untuk input inggris

# Membuat tombol submit
Button(root, text="Submit", command=submit, bg="#B9E5E8", font=("Comic Sans MS", 10)).grid(row=4, column=0, padx=10, pady=10)
# Membuat tombol update
Button(root, text="Update", command=update, bg="#B9E5E8", font=("Comic Sans MS", 10)).grid(row=4, column=1, padx=10, pady=10)
# Membuat tombol delete
Button(root, text="Delete", command=delete, bg="#B9E5E8", font=("Comic Sans MS", 10)).grid(row=4, column=2, padx=10, pady=10)

# Membuat Treeview untuk menampilkan data
tree = ttk.Treeview(root, columns=("ID", "Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas"), show='headings')
tree.heading("ID", text="ID") # Mengatur header kolom ID
tree.heading("Nama Siswa", text="Nama Siswa") # Mengatur header kolom Nama Siswa
tree.heading("Biologi", text="Biologi") # Mengatur header kolom Biologi
tree.heading("Fisika", text="Fisika") # Mengatur header kolom Fisika    
tree.heading("Inggris", text="Inggris") # Mengatur header kolom Inggris
tree.heading("Prediksi Fakultas", text="Prediksi Fakultas") # Mengatur header kolom Prediksi Fakultas
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10) # Menampilkan Treeview   

# Menghubungkan event klik pada Treeview dengan fungsi
tree.bind("<ButtonRelease-1>", fill_inputs_from_table) # Menghubungkan event klik pada Treeview dengan fungsi fill_inputs_from_table

root.mainloop() # Menjalankan loop utama Tkinter    


