import tkinter as tk
from tkinter import *
from tkinter import ttk, Label, messagebox
import os
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
import mysql.connector
from tkcalendar import DateEntry
import re
import random

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("System Management Smart Money")
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.state('zoomed')
        self.root.config(background='#009aa5')

        # Koneksi ke database
        self.db_connection = mysql.connector.connect(
            host="localhost",  # ganti dengan host database Anda
            user="root",       # ganti dengan username database Anda
            password="",       # ganti dengan password database Anda
            database="pbd6"
        )
        self.db_cursor = self.db_connection.cursor()

        # Sidebar
        self.sidebar = Frame(self.root, bg='#005f6a')
        self.sidebar.place(x=0, y=0, width=250, height=850)

        clock_frame = tk.Frame(self.sidebar, bg="#005f6a")
        clock_frame.place(x=0, y=10, width=200, height=50)

        self.date_time_label = tk.Label(clock_frame, bg="#005f6a", fg="white", font=("", 13, "bold"))
        self.date_time_label.place(x=0, y=0, width=200, height=50)

        self.update_time()

        profile_frame = tk.Frame(self.sidebar, bg="#005f6a")
        profile_frame.place(x=0, y=70, width=200, height=50)

        profile_label = tk.Label(profile_frame, text="Arul Hidayat", bg="#005f6a", fg="white", font=("Arial", 12, "bold"))
        profile_label.place(x=0, y=0, width=200, height=50)

        self.dashboardImage = ImageTk.PhotoImage(file='images/dashboard-solid-24 (1).png')
        self.dashboard = Label(self.sidebar, image=self.dashboardImage, bg='#005f6a')
        self.dashboard.place(x=35, y=200)

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#005f6a',command=self.open_dashboard)
        self.dashboard_text.place(x=80, y=200)

        self.manageImage1 = ImageTk.PhotoImage(file='images/horizontal-right-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage1, bg='#005f6a')
        self.manage.place(x=35, y=240)

        self.manage_text = Button(self.sidebar, text="Pemasukan", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a',command=self.open_pemasukan)
        self.manage_text.place(x=80, y=240)

        self.manageImage = ImageTk.PhotoImage(file='images/horizontal-left-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage, bg='#005f6a')
        self.manage.place(x=35, y=280)

        self.manage_text = Button(self.sidebar, text="Pengeluaran", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a', command=self.open_pengeluaran)
        self.manage_text.place(x=80, y=280)

        # Body
        self.heading = Label(self.root, text='Dashboard', font=("", 15, "bold"), fg='white', bg='#009aa5')
        self.heading.place(x=325, y=70)

        self.bodyFrame1 = Frame(self.root, bg='#ffffff')
        self.bodyFrame1.place(x=328, y=110, width=1040, height=350)

        self.bodyFrame5 = Frame(self.root, bg='#009aa5')
        self.bodyFrame5.place(x=350, y=160, width=300, height=250)

        self.bodyFrame6 = Frame(self.root, bg='#009aa5')
        self.bodyFrame6.place(x=700, y=160, width=300, height=250)

        self.bodyFrame7 = Frame(self.root, bg='#009aa5')
        self.bodyFrame7.place(x=1050, y=160, width=300, height=250)

        # Frame 5 judul
        self.saldo_label = Label(self.bodyFrame5, text="Saldo", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.saldo_label.place(x=5, y=5)
        self.saldo_value = Label(self.bodyFrame5, text="", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.saldo_value.place(x=5, y=50)

        # Frame 6 judul
        self.pemasukan_label = Label(self.bodyFrame6, text="Pemasukan", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.pemasukan_label.place(x=5, y=5)
        self.pemasukan_value = Label(self.bodyFrame6, text="", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.pemasukan_value.place(x=5, y=50)

        # Frame 7 judul
        self.pengeluaran_label = Label(self.bodyFrame7, text="Pengeluaran", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.pengeluaran_label.place(x=5, y=5)
        self.pengeluaran_value = Label(self.bodyFrame7, text="", bg='#009aa5', font=("", 14, "bold"), fg='white')
        self.pengeluaran_value.place(x=5, y=50)

        self.update_financial_data()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        self.date_time_label.config(text=f"{current_time}\n{current_date}")
        self.root.after(1000, self.update_time)

    def update_financial_data(self):
        # Mengambil data pemasukan
        self.db_cursor.execute("SELECT SUM(Jumlah) FROM pemasukan")
        total_pemasukan = self.db_cursor.fetchone()[0] or 0

        # Mengambil data pengeluaran
        self.db_cursor.execute("SELECT SUM(Jumlah) FROM pengeluaran")
        total_pengeluaran = self.db_cursor.fetchone()[0] or 0

        # Menghitung saldo
        saldo = total_pemasukan - total_pengeluaran

        # Memperbarui label
        self.saldo_value.config(text=f"Rp {saldo:,}")
        self.pemasukan_value.config(text=f"Rp {total_pemasukan:,}")
        self.pengeluaran_value.config(text=f"Rp {total_pengeluaran:,}")
            
    def open_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Dashboard(self.root)
    
    def open_pemasukan(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pemasukan(self.root)
    
    def open_pengeluaran(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pengeluaran(self.root)
    

class Pemasukan:
    def __init__(self, root):
        self.root = root
        self.root.title("System Management Smart Money")
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.state('zoomed')
        self.root.config(background='#009aa5')

        # Connect to database and create table if it doesn't exist
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pbd6"
        )
        self.create_table()

        # Sidebar setup
        self.sidebar = Frame(self.root, bg='#005f6a')
        self.sidebar.place(x=0, y=0, width=250, height=850)

        # Date and time display at the top of the sidebar
        clock_frame = tk.Frame(self.sidebar, bg="#005f6a")
        clock_frame.place(x=0, y=10, width=200, height=50)

        self.date_time_label = tk.Label(clock_frame, bg="#005f6a", fg="white", font=("", 13, "bold"))
        self.date_time_label.place(x=0, y=0, width=200, height=50)

        self.update_time()

        profile_frame = tk.Frame(self.sidebar, bg="#005f6a")
        profile_frame.place(x=0, y=70, width=200, height=50)

        profile_label = tk.Label(profile_frame, text="Arul Hidayat", bg="#005f6a", fg="white", font=("Arial", 12, "bold"))
        profile_label.place(x=0, y=0, width=200, height=50)

        # Dashboard_button
        self.dashboardImage = ImageTk.PhotoImage(file='images/dashboard-solid-24 (1).png')
        self.dashboard = Label(self.sidebar, image=self.dashboardImage, bg='#005f6a')
        self.dashboard.place(x=35, y=200)

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#005f6a',command=self.open_dashboard)
        self.dashboard_text.place(x=80, y=200)

        # Pemasukan_button
        self.manageImage1 = ImageTk.PhotoImage(file='images/horizontal-right-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage1, bg='#005f6a')
        self.manage.place(x=35, y=240)

        self.manage_text = Button(self.sidebar, text="Pemasukan", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a', command=self.open_pemasukan)
        self.manage_text.place(x=80, y=240)

        # Pengeluaran_button
        self.manageImage = ImageTk.PhotoImage(file='images/horizontal-left-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage, bg='#005f6a')
        self.manage.place(x=35, y=280)

        self.manage_text = Button(self.sidebar, text="Pengeluaran", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a', command=self.open_pengeluaran)
        self.manage_text.place(x=80, y=280)

        # Main content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.place(x=250, y=0, width=1350, height=850)

        header = tk.Frame(self.content_frame, bg="#d9edf7")
        header.place(x=0, y=0, width=1350, height=100)

        # Add labels and buttons
        title = tk.Label(header, text="Pemasukan", bg="#d9edf7", font=('Arial', 16, 'bold'))
        title.place(x=20, y=20)

        data_title = tk.Label(header, text="Data Pemasukan", bg="#d9edf7", font=('Arial', 12, 'bold'))
        data_title.place(x=20, y=60)

        search_button = tk.Button(header, text="Cari", command=self.handle_search)
        search_button.place(x=850, y=60)

        self.search_entry = tk.Entry(header)
        self.search_entry.place(x=900, y=60)

        self.add_pemasukan()
        self.show_pemasukan()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        self.date_time_label.config(text=f"{current_time}\n{current_date}")
        self.root.after(1000, self.update_time)

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pemasukan (
        No INT AUTO_INCREMENT PRIMARY KEY,
        Kode VARCHAR(255) UNIQUE,
        Tanggal DATE,
        Kategori_Pemasukan VARCHAR(255),
        Deskripsi_Transaksi VARCHAR(255),
        Jumlah INT(10)
        )
        """)
        self.db.commit()

    def show_pemasukan(self):
        # Treeview for data display
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        columns = ("Kode", "Tanggal", "Kategori Pemasukan", "Deskripsi Transaksi", "Jumlah")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.place(x=0, y=310, width=1050, height=648)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)  # Bind the treeview select event

        self.load_data()

    def load_data(self):
        if not self.db:
            messagebox.showerror("Database Error", "No database connection available")
            return

        self.clear_tree()
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM pemasukan")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row[1:])
        cursor.close()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, 'values')
        self.entries["Kode"].delete(0, tk.END)
        self.entries["Kode"].insert(0, item_values[0])
        self.entries["Tanggal"].set_date(item_values[1])
        self.entries["Kategori Pemasukan"].set(item_values[2])
        self.entries["Deskripsi Transaksi"].delete(0, tk.END)
        self.entries["Deskripsi Transaksi"].insert(0, item_values[3])
        self.entries["Jumlah"].delete(0, tk.END)
        self.entries["Jumlah"].insert(0, item_values[4])

    def validate_rupiah_input(self, value):
        if re.match(r'^[0-9,.]+$', value) or value == "":
            return True
        else:
            self.root.bell()  # Emit a beep sound for invalid input
            return False

    def save_data(self):
        try:
            kode = self.entries["Kode"].get()
            tanggal = self.entries["Tanggal"].get()
            kategori_pemasukan = self.entries["Kategori Pemasukan"].get()
            deskripsi_transaksi = self.entries["Deskripsi Transaksi"].get()
            jumlah = self.entries["Jumlah"].get()

            self.simpan(kode, tanggal, kategori_pemasukan, deskripsi_transaksi, jumlah)
            self.load_data()  # Refresh data after saving
        except KeyError as e:
            messagebox.showerror("Error", f"Entry not found: {e}")

    def simpan(self, kode, tanggal, kategori_pemasukan, deskripsi_transaksi, jumlah):
        try:
            cursor = self.db.cursor()
            sql_saya = """
            INSERT INTO pemasukan (Kode, Tanggal, Kategori_Pemasukan, Deskripsi_Transaksi, Jumlah)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_saya, (kode, tanggal, kategori_pemasukan, deskripsi_transaksi, jumlah))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data inserted successfully")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_data(self):
        try:
            kode = self.entries["Kode"].get()
            if not kode:
                messagebox.showerror("Error", "Kode harus diisi untuk mengedit data")
                return

            cursor = self.db.cursor()

            tanggal = self.entries["Tanggal"].get()
            kategori_pemasukan = self.entries["Kategori Pemasukan"].get()
            deskripsi_transaksi = self.entries["Deskripsi Transaksi"].get()
            jumlah = self.entries["Jumlah"].get()

            updates = []
            values = []

            if tanggal:
                updates.append("Tanggal = %s")
                values.append(tanggal)
            if kategori_pemasukan:
                updates.append("Kategori_Pemasukan = %s")
                values.append(kategori_pemasukan)
            if deskripsi_transaksi:
                updates.append("Deskripsi_Transaksi = %s")
                values.append(deskripsi_transaksi)
            if jumlah:
                updates.append("Jumlah = %s")
                values.append(jumlah)

            if not updates:
                messagebox.showerror("Error", "Tidak ada kolom yang diisi untuk diubah")
                return

            values.append(kode)
            sql_saya = f"UPDATE pemasukan SET {', '.join(updates)} WHERE Kode = %s"
            cursor.execute(sql_saya, values)
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data updated successfully")
            self.clear_form()
            self.load_data()  # Refresh data after editing
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_data(self):
        try:
            kode = self.entries["Kode"].get()
            if not kode:
                messagebox.showerror("Error", "Kode harus diisi untuk menghapus data")
                return

            cursor = self.db.cursor()
            sql_saya = "DELETE FROM pemasukan WHERE Kode = %s"
            cursor.execute(sql_saya, (kode,))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data deleted successfully")
            self.clear_form()
            self.load_data()  # Refresh data after deleting
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, StringVar):
                entry.set("Pilih kategori")
            elif isinstance(entry, DateEntry):
                entry.set_date("")

    def add_pemasukan(self):
        form_frame = tk.Frame(self.content_frame, bg="#d9edf7", bd=2, relief="groove")
        form_frame.place(x=0, y=100, width=1290, height=212)

        label_texts = ["Kode", "Tanggal", "Kategori Pemasukan", "Deskripsi Transaksi", "Jumlah"]
        self.entries = {}

        # Buat list kategori
        kategori_options = ["Pilih kategori", "Deposito", "Dividen", "Gaji", "Hibah", "Investasi", "Kupon", "Lain-lain", "Pengembalian Dana", "Penghargaan", "Penjualan", "Penyewaan", "Tabungan"]

        for i, text in enumerate(label_texts):
            lbl = tk.Label(form_frame, text=text, bg="#d9edf7", fg="black", font=("Helvetica", 10), anchor="w")
            lbl.place(x=20, y=20 + i * 40)

            if text == "Kategori Pemasukan":
                # Gunakan menu dropdown
                selected_kategori = tk.StringVar(self.root)
                selected_kategori.set(kategori_options[0])  # Set default selection

                kategori_menu = tk.OptionMenu(form_frame, selected_kategori, *kategori_options)
                kategori_menu.config(font=("Helvetica", 10))
                kategori_menu.place(x=175, y=20 + i * 40)
                self.entries[text] = selected_kategori

            else:
                entry = tk.Entry(form_frame, width=30, font=("Helvetica", 10))
                if text == "Kode":
                    entry = tk.Entry(form_frame, width=15, font=("Helvetica", 10))
                elif text == "Tanggal":
                    entry = DateEntry(form_frame, width=12, font=("Helvetica", 10), date_pattern='yyyy-mm-dd')
                elif text == "Jumlah":
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(self.root.register(self.validate_rupiah_input), "%P"))
                entry.place(x=175, y=20 + i * 40)
                self.entries[text] = entry

        random_button = tk.Button(form_frame, text="Generate Kode", bg="white", fg="black", font=("Helvetica", 10), width=12, command=self.fill_kode_entry)
        random_button.place(x=300, y=15)

        button_frame = tk.Frame(form_frame, bg="#d9edf7")
        button_frame.place(x=550, y=55)

        simpan_button = tk.Button(button_frame, text="Simpan", bg="#3c78d8", fg="white", font=("Helvetica", 10), width=10, command=self.save_data)
        simpan_button.pack(side="top", pady=5)

        edit_button = tk.Button(button_frame, text="Edit", bg="#00BF63", fg="white", font=("Helvetica", 10), width=10, command=self.edit_data)
        edit_button.pack(side="top", pady=5)

        hapus_button = tk.Button(button_frame, text="Hapus", bg="#e06666", fg="white", font=("Helvetica", 10), width=10, command=self.delete_data)
        hapus_button.pack(side="top", pady=5)

    def generateRand(self):
        numeric = '1234567890'
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        kode = ''
        for i in range(0, 3):
            randno = random.randrange(0, len(numeric))
            kode += numeric[randno]
        randno = random.randrange(0, len(alpha))
        kode += '-' + alpha[randno]
        print("Generated Kode:", kode)  # Debugging line
        return kode

    def fill_kode_entry(self):
        generated_kode = self.generateRand()
        print("Filling Kode Entry with:", generated_kode)  # Debugging line
        kode_entry = self.entries.get("Kode")
        if kode_entry:
            kode_entry.delete(0, tk.END)
            kode_entry.insert(0, generated_kode)
        else:
            print("Kode entry not found!")

    def handle_search(self):
        search_value = self.search_entry.get()
        if not search_value:
            messagebox.showerror("Error", "Silakan masukkan nilai untuk mencari.")
            return

        cursor = self.db.cursor()
        query = """
        SELECT Kode, Tanggal, Kategori_Pemasukan, Deskripsi_Transaksi, Jumlah
        FROM pemasukan
        WHERE Kode LIKE %s OR
              Tanggal LIKE %s OR
              Kategori_Pemasukan LIKE %s OR
              Deskripsi_Transaksi LIKE %s OR
              Jumlah LIKE %s
        """
        like_value = f"%{search_value}%"
        cursor.execute(query, (like_value, like_value, like_value, like_value, like_value))
        rows = cursor.fetchall()
        cursor.close()

        self.clear_tree()
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def open_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Dashboard(self.root)

    def open_pemasukan(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pemasukan(self.root)

    def open_pengeluaran(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pengeluaran(self.root)
       
class Pengeluaran:
    def __init__(self, root):
        self.root = root
        self.root.title("System Management Smart Money")
        self.root.geometry("1366x768")
        self.root.resizable(0, 0)
        self.root.state('zoomed')
        self.root.config(background='#009aa5')

        # Connect to database and create table if it doesn't exist
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pbd6"
        )
        self.create_table()

        # Sidebar setup
        self.sidebar = Frame(self.root, bg='#005f6a')
        self.sidebar.place(x=0, y=0, width=250, height=850)

        # Date and time display at the top of the sidebar
        clock_frame = tk.Frame(self.sidebar, bg="#005f6a")
        clock_frame.place(x=0, y=10, width=200, height=50)

        self.date_time_label = tk.Label(clock_frame, bg="#005f6a", fg="white", font=("", 13, "bold"))
        self.date_time_label.place(x=0, y=0, width=200, height=50)

        self.update_time()

        profile_frame = tk.Frame(self.sidebar, bg="#005f6a")
        profile_frame.place(x=0, y=70, width=200, height=50)

        profile_label = tk.Label(profile_frame, text="Arul Hidayat", bg="#005f6a", fg="white", font=("Arial", 12, "bold"))
        profile_label.place(x=0, y=0, width=200, height=50)

        # Dashboard_button
        self.dashboardImage = ImageTk.PhotoImage(file='images/dashboard-solid-24 (1).png')
        self.dashboard = Label(self.sidebar, image=self.dashboardImage, bg='#005f6a')
        self.dashboard.place(x=35, y=200)

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#005f6a',command=self.open_dashboard)
        self.dashboard_text.place(x=80, y=200)

        # Pemasukan_button
        self.manageImage1 = ImageTk.PhotoImage(file='images/horizontal-right-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage1, bg='#005f6a')
        self.manage.place(x=35, y=240)

        self.manage_text = Button(self.sidebar, text="Pemasukan", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a', command=self.open_pemasukan)
        self.manage_text.place(x=80, y=240)

        # Pengeluaran_button
        self.manageImage = ImageTk.PhotoImage(file='images/horizontal-left-regular-24 (1).png')
        self.manage = Label(self.sidebar, image=self.manageImage, bg='#005f6a')
        self.manage.place(x=35, y=280)

        self.manage_text = Button(self.sidebar, text="Pengeluaran", bg='#005f6a', fg="white", font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#005f6a', command=self.open_pengeluaran)
        self.manage_text.place(x=80, y=280)

        # Main content frame
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.place(x=250, y=0, width=1350, height=850)

        header = tk.Frame(self.content_frame, bg="#d9edf7")
        header.place(x=0, y=0, width=1350, height=100)

        # Add labels and buttons
        title = tk.Label(header, text="Pengeluaran", bg="#d9edf7", font=('Arial', 16, 'bold'))
        title.place(x=20, y=20)

        data_title = tk.Label(header, text="Data Pengeluaran", bg="#d9edf7", font=('Arial', 12, 'bold'))
        data_title.place(x=20, y=60)

        search_button = tk.Button(header, text="Cari", command=self.handle_search)
        search_button.place(x=850, y=60)

        self.search_entry = tk.Entry(header)
        self.search_entry.place(x=900, y=60)

        self.add_pengeluaran()
        self.show_pengeluaran()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        self.date_time_label.config(text=f"{current_time}\n{current_date}")
        self.root.after(1000, self.update_time)

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengeluaran (
        No INT AUTO_INCREMENT PRIMARY KEY,
        Kode VARCHAR(255) UNIQUE,
        Tanggal DATE,
        Kategori_Pengeluaran VARCHAR(255),
        Deskripsi_Transaksi VARCHAR(255),
        Jumlah INT(10)
        )
        """)
        self.db.commit()

    def show_pengeluaran(self):
        # Treeview for data display
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        columns = ("Kode", "Tanggal", "Kategori Pengeluaran", "Deskripsi Transaksi", "Jumlah")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.place(x=0, y=310, width=1050, height=648)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)  # Bind the treeview select event

        self.load_data()

    def load_data(self):
        if not self.db:
            messagebox.showerror("Database Error", "No database connection available")
            return

        self.clear_tree()
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM pengeluaran")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert('', 'end', values=row[1:])
        cursor.close()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, 'values')
        self.entries["Kode"].delete(0, tk.END)
        self.entries["Kode"].insert(0, item_values[0])
        self.entries["Tanggal"].set_date(item_values[1])
        self.entries["Kategori Pengeluaran"].set(item_values[2])
        self.entries["Deskripsi Transaksi"].delete(0, tk.END)
        self.entries["Deskripsi Transaksi"].insert(0, item_values[3])
        self.entries["Jumlah"].delete(0, tk.END)
        self.entries["Jumlah"].insert(0, item_values[4])

    def validate_rupiah_input(self, value):
        if re.match(r'^[0-9,.]+$', value) or value == "":
            return True
        else:
            self.root.bell()  # Emit a beep sound for invalid input
            return False

    def save_data(self):
        try:
            kode = self.entries["Kode"].get()
            tanggal = self.entries["Tanggal"].get()
            kategori_pengeluaran = self.entries["Kategori Pengeluaran"].get()
            deskripsi_transaksi = self.entries["Deskripsi Transaksi"].get()
            jumlah = self.entries["Jumlah"].get()

            self.simpan(kode, tanggal, kategori_pengeluaran, deskripsi_transaksi, jumlah)
            self.load_data()  # Refresh data after saving
        except KeyError as e:
            messagebox.showerror("Error", f"Entry not found: {e}")

    def simpan(self, kode, tanggal, kategori_pengeluaran, deskripsi_transaksi, jumlah):
        try:
            cursor = self.db.cursor()
            sql_saya = """
            INSERT INTO pengeluaran (Kode, Tanggal, Kategori_Pengeluaran, Deskripsi_Transaksi, Jumlah)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_saya, (kode, tanggal, kategori_pengeluaran, deskripsi_transaksi, jumlah))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data inserted successfully")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_data(self):
        try:
            kode = self.entries["Kode"].get()
            if not kode:
                messagebox.showerror("Error", "Kode harus diisi untuk mengedit data")
                return

            cursor = self.db.cursor()

            tanggal = self.entries["Tanggal"].get()
            kategori_pengeluaran = self.entries["Kategori Pengeluaran"].get()
            deskripsi_transaksi = self.entries["Deskripsi Transaksi"].get()
            jumlah = self.entries["Jumlah"].get()

            updates = []
            values = []

            if tanggal:
                updates.append("Tanggal = %s")
                values.append(tanggal)
            if kategori_pengeluaran:
                updates.append("Kategori_Pengeluaran = %s")
                values.append(kategori_pengeluaran)
            if deskripsi_transaksi:
                updates.append("Deskripsi_Transaksi = %s")
                values.append(deskripsi_transaksi)
            if jumlah:
                updates.append("Jumlah = %s")
                values.append(jumlah)

            if not updates:
                messagebox.showerror("Error", "Tidak ada kolom yang diisi untuk diubah")
                return

            values.append(kode)
            sql_saya = f"UPDATE pengeluaran SET {', '.join(updates)} WHERE Kode = %s"
            cursor.execute(sql_saya, values)
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data updated successfully")
            self.clear_form()
            self.load_data()  # Refresh data after editing
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_data(self):
        try:
            kode = self.entries["Kode"].get()
            if not kode:
                messagebox.showerror("Error", "Kode harus diisi untuk menghapus data")
                return

            cursor = self.db.cursor()
            sql_saya = "DELETE FROM pengeluaran WHERE Kode = %s"
            cursor.execute(sql_saya, (kode,))
            self.db.commit()
            cursor.close()
            messagebox.showinfo("Success", "Data deleted successfully")
            self.clear_form()
            self.load_data()  # Refresh data after deleting
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        for entry in self.entries.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, StringVar):
                entry.set("Pilih kategori")
            elif isinstance(entry, DateEntry):
                entry.set_date("")

    def add_pengeluaran(self):
        form_frame = tk.Frame(self.content_frame, bg="#d9edf7", bd=2, relief="groove")
        form_frame.place(x=0, y=100, width=1290, height=212)

        label_texts = ["Kode", "Tanggal", "Kategori Pengeluaran", "Deskripsi Transaksi", "Jumlah"]
        self.entries = {}

        # Buat list kategori
        kategori_options = ["Pilih kategori", "Asuransi", "Belanja", "Elektronik", "Hadiah", "Hewan Peliharaan", "Hiburan", "Kantor", "Kecantikan", "Kesehatan", "Lain-lain", "Makanan", "Mobil", "Motor", "Olahraga", "Pajak", "Pakaian", "Pendidikan", "Pulsa", "Rokok", "Rumah", "Sosial", "Tagihan"]

        for i, text in enumerate(label_texts):
            lbl = tk.Label(form_frame, text=text, bg="#d9edf7", fg="black", font=("Helvetica", 10), anchor="w")
            lbl.place(x=20, y=20 + i * 40)

            if text == "Kategori Pengeluaran":
                # Gunakan menu dropdown
                selected_kategori = tk.StringVar(self.root)
                selected_kategori.set(kategori_options[0])  # Set default selection

                kategori_menu = tk.OptionMenu(form_frame, selected_kategori, *kategori_options)
                kategori_menu.config(font=("Helvetica", 10))
                kategori_menu.place(x=175, y=20 + i * 40)
                self.entries[text] = selected_kategori

            else:
                entry = tk.Entry(form_frame, width=30, font=("Helvetica", 10))
                if text == "Kode":
                    entry = tk.Entry(form_frame, width=15, font=("Helvetica", 10))
                elif text == "Tanggal":
                    entry = DateEntry(form_frame, width=12, font=("Helvetica", 10), date_pattern='yyyy-mm-dd')
                elif text == "Jumlah":
                    entry.configure(validate="key")
                    entry.configure(validatecommand=(self.root.register(self.validate_rupiah_input), "%P"))
                entry.place(x=175, y=20 + i * 40)
                self.entries[text] = entry

        random_button = tk.Button(form_frame, text="Generate Kode", bg="white", fg="black", font=("Helvetica", 10), width=12, command=self.fill_kode_entry)
        random_button.place(x=300, y=15)

        button_frame = tk.Frame(form_frame, bg="#d9edf7")
        button_frame.place(x=550, y=55)

        simpan_button = tk.Button(button_frame, text="Simpan", bg="#3c78d8", fg="white", font=("Helvetica", 10), width=10, command=self.save_data)
        simpan_button.pack(side="top", pady=5)

        edit_button = tk.Button(button_frame, text="Edit", bg="#00BF63", fg="white", font=("Helvetica", 10), width=10, command=self.edit_data)
        edit_button.pack(side="top", pady=5)

        hapus_button = tk.Button(button_frame, text="Hapus", bg="#e06666", fg="white", font=("Helvetica", 10), width=10, command=self.delete_data)
        hapus_button.pack(side="top", pady=5)

    def generateRand(self):
        numeric = '1234567890'
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        kode = ''
        for i in range(0, 3):
            randno = random.randrange(0, len(numeric))
            kode += numeric[randno]
        randno = random.randrange(0, len(alpha))
        kode += '-' + alpha[randno]
        print("Generated Kode:", kode)  # Debugging line
        return kode

    def fill_kode_entry(self):
        generated_kode = self.generateRand()
        print("Filling Kode Entry with:", generated_kode)  # Debugging line
        kode_entry = self.entries.get("Kode")
        if kode_entry:
            kode_entry.delete(0, tk.END)
            kode_entry.insert(0, generated_kode)
        else:
            print("Kode entry not found!")

    def handle_search(self):
        search_value = self.search_entry.get()
        if not search_value:
            messagebox.showerror("Error", "Silakan masukkan nilai untuk mencari.")
            return

        cursor = self.db.cursor()
        query = """
        SELECT Kode, Tanggal, Kategori_Pengeluaran, Deskripsi_Transaksi, Jumlah
        FROM pengeluaran
        WHERE Kode LIKE %s OR
              Tanggal LIKE %s OR
              Kategori_Pengeluaran LIKE %s OR
              Deskripsi_Transaksi LIKE %s OR
              Jumlah LIKE %s
        """
        like_value = f"%{search_value}%"
        cursor.execute(query, (like_value, like_value, like_value, like_value, like_value))
        rows = cursor.fetchall()
        cursor.close()

        self.clear_tree()
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def open_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Dashboard(self.root)

    def open_pemasukan(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pemasukan(self.root)

    def open_pengeluaran(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        Pengeluaran(self.root)

# Fungsi utama
def main():
    global root
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()