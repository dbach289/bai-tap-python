from tkinter import messagebox

def them(cursor, conn, data, load_data):
    try:
        cursor.execute("INSERT INTO nhansu VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        messagebox.showinfo("OK", "Thêm thành công")
        load_data()
    except:
        messagebox.showerror("Lỗi", "CCCD đã tồn tại!")

def sua(cursor, conn, data, load_data):
    cursor.execute("""
    UPDATE nhansu SET ten=?, ngaysinh=?, gioitinh=?, diachi=?
    WHERE cccd=?
    """, (data[1], data[2], data[3], data[4], data[0]))

    conn.commit()
    messagebox.showinfo("OK", "Sửa thành công")
    load_data()

def xoa(cursor, conn, cccd, load_data):
    cursor.execute("DELETE FROM nhansu WHERE cccd=?", (cccd,))
    conn.commit()
    messagebox.showinfo("OK", "Xóa thành công")
    load_data()

def tim(cursor, keyword):
    cursor.execute("""
    SELECT * FROM nhansu
    WHERE cccd LIKE ? OR ten LIKE ? OR diachi LIKE ?
    """, ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))

    return cursor.fetchall()

def get_all(cursor):
    cursor.execute("SELECT * FROM nhansu")
    return cursor.fetchall()