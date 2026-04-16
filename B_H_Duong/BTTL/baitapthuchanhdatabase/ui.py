import customtkinter as ctk
from tkinter import ttk
from functions import *

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, cursor, conn):
        super().__init__()

        self.cursor = cursor
        self.conn = conn

        self.title("Quản lý nhân sự")
        self.geometry("1000x600")

        self.create_ui()
        self.load_data()

    def create_ui(self):
        # ===== TITLE =====
        title = ctk.CTkLabel(self, text="QUẢN LÝ NHÂN SỰ", font=("Arial", 22, "bold"))
        title.pack(pady=15)

        # ===== FORM =====
        form = ctk.CTkFrame(self)
        form.pack(padx=20, pady=10, fill="x")

        # chia đều cột
        for i in range(6):
            form.grid_columnconfigure(i, weight=1)

        # ROW 1
        ctk.CTkLabel(form, text="CCCD").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.cccd = ctk.CTkEntry(form)
        self.cccd.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form, text="Họ tên").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.ten = ctk.CTkEntry(form)
        self.ten.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form, text="Ngày sinh").grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.ngaysinh = ctk.CTkEntry(form)
        self.ngaysinh.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

        # ROW 2
        ctk.CTkLabel(form, text="Giới tính").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.gioitinh = ctk.CTkComboBox(form, values=["Nam", "Nữ"])
        self.gioitinh.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form, text="Địa chỉ").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.diachi = ctk.CTkEntry(form)
        self.diachi.grid(row=1, column=3, columnspan=3, padx=10, pady=10, sticky="ew")

        # ===== BUTTON =====
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=15)

        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkButton(btn_frame, text="Thêm", width=120, command=self.them)\
            .grid(row=0, column=0, padx=15)

        ctk.CTkButton(btn_frame, text="Sửa", width=120, command=self.sua)\
            .grid(row=0, column=1, padx=15)

        ctk.CTkButton(btn_frame, text="Xóa", width=120, command=self.xoa)\
            .grid(row=0, column=2, padx=15)

        # ===== SEARCH =====
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=10)

        self.search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nhập CCCD / tên / địa chỉ",
            width=300
        )
        self.search.grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(search_frame, text="Tìm kiếm", command=self.tim)\
            .grid(row=0, column=1, padx=10)

        # ===== TABLE =====
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("cccd", "ten", "ngaysinh", "gioitinh", "diachi")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("cccd", text="CCCD")
        self.tree.heading("ten", text="Họ tên")
        self.tree.heading("ngaysinh", text="Ngày sinh")
        self.tree.heading("gioitinh", text="Giới tính")
        self.tree.heading("diachi", text="Địa chỉ")

        self.tree.column("cccd", width=120)
        self.tree.column("ten", width=200)
        self.tree.column("ngaysinh", width=120)
        self.tree.column("gioitinh", width=100)
        self.tree.column("diachi", width=300)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.select)

    # ===== DATA =====
    def get_data(self):
        return (
            self.cccd.get(),
            self.ten.get(),
            self.ngaysinh.get(),
            self.gioitinh.get(),
            self.diachi.get()
        )

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in get_all(self.cursor):
            self.tree.insert("", "end", values=row)

    def them(self):
        them(self.cursor, self.conn, self.get_data(), self.load_data)

    def sua(self):
        sua(self.cursor, self.conn, self.get_data(), self.load_data)

    def xoa(self):
        xoa(self.cursor, self.conn, self.cccd.get(), self.load_data)

    def tim(self):
        data = tim(self.cursor, self.search.get())

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in data:
            self.tree.insert("", "end", values=row)

    def select(self, event):
        item = self.tree.focus()
        data = self.tree.item(item, "values")

        if data:
            self.cccd.delete(0, "end")
            self.cccd.insert(0, data[0])

            self.ten.delete(0, "end")
            self.ten.insert(0, data[1])

            self.ngaysinh.delete(0, "end")
            self.ngaysinh.insert(0, data[2])

            self.gioitinh.set(data[3])

            self.diachi.delete(0, "end")
            self.diachi.insert(0, data[4])