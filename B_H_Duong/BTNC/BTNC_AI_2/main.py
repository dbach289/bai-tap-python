# ================== IMPORT ==================
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Import các module đã tách
from bai_handler import tach_bai, tao_file
from github_handler import push_github
from ai_handler import ask_ai  

# ================== CẤU HÌNH ==================
HISTORY_FILE = "chat_history.txt"
last_code = ""  # lưu code gần nhất

# ================== TẠO CỬA SỔ ==================
root = tk.Tk()
root.title("AI Tự Động Làm Bài Python + GitHub")
root.geometry("1000x750")
root.configure(bg="#0f172a")

FONT = ("Segoe UI", 11)

# ================== MODEL ==================
model_var = tk.StringVar(value="llama-3.3-70b-versatile")

MODEL_INFO = {
    "llama-3.1-8b-instant": "Nhanh | Trung bình",
    "llama-3.3-70b-versatile": "Chậm hơn | Rất thông minh"
}

# ================== HEADER ==================
header = tk.Frame(root, bg="#020617", height=50)
header.pack(fill="x")

tk.Label(header,
         text="AI HỖ TRỢ LÀM BÀI PYTHON",
         fg="#22c55e",
         bg="#020617",
         font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

# ===== chọn model =====
model_frame = tk.Frame(header, bg="#020617")
model_frame.pack(side="right", padx=10)

tk.Label(model_frame,
         text="Model:",
         fg="white",
         bg="#020617",
         font=FONT).pack(side="left")

model_menu = tk.OptionMenu(model_frame,
                           model_var,
                           "llama-3.3-70b-versatile",
                           "llama-3.1-8b-instant")

model_menu.config(bg="#1e293b", fg="white", font=FONT)
model_menu.pack(side="left", padx=5)

model_info = tk.Label(header,
                      text=MODEL_INFO[model_var.get()],
                      fg="#94a3b8",
                      bg="#020617",
                      font=("Segoe UI", 9))

model_info.pack(side="right", padx=10)

def update_model(*args):
    model_info.config(text=MODEL_INFO[model_var.get()])

model_var.trace("w", update_model)

# ================== KHUNG CHAT ==================
chat_frame = tk.Frame(root, bg="#0f172a")
chat_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")

chat_box = tk.Text(chat_frame,
                   bg="#020617",
                   fg="#e2e8f0",
                   font=FONT,
                   wrap="word",
                   yscrollcommand=scrollbar.set)

chat_box.pack(fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=chat_box.yview)

chat_box.config(state="disabled")

# ===== màu =====
chat_box.tag_config("user", foreground="#38bdf8")
chat_box.tag_config("ai", foreground="#22c55e")
chat_box.tag_config("code", foreground="#facc15")

# ================== HÀM CHAT ==================
def add_chat(text, tag=None):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, text + "\n\n", tag)
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, f.read())
            chat_box.config(state="disabled")

# ================== GỬI CHAT ==================
def send_chat():
    global last_code

    text = entry.get().strip()

    if not text:
        return

    status.config(text="🤖 AI đang trả lời...", fg="yellow")
    root.update()

    add_chat("Bạn: " + text, "user")

    try:
        code = ask_ai(text, model_var.get())

        last_code = code

        add_chat(code, "code")

        status.config(text="✅ Xong", fg="#22c55e")

    except Exception as e:
        add_chat("❌ Lỗi: " + str(e), "ai")
        status.config(text="Lỗi", fg="red")

    entry.delete(0, tk.END)

def auto_bai():
    global last_code

    text = entry.get().strip()

    if not text:
        messagebox.showwarning("Lỗi", "Nhập đề bài!")
        return

    # chọn thư mục
    folder = filedialog.askdirectory(title="Chọn thư mục lưu bài")

    if not folder:
        add_chat("❌ Bạn chưa chọn thư mục", "ai")
        return

    status.config(text="⏳ Đang xử lý...", fg="yellow")
    root.update()

    add_chat("Bạn (Auto): " + text, "user")

    try:
        ds_bai = tach_bai(text)

        if not isinstance(ds_bai, list) or not ds_bai:
            add_chat("❌ Không nhận diện được bài", "ai")
            status.config(text="Lỗi", fg="red")
            return

        add_chat(f"📚 Tìm thấy {len(ds_bai)} bài", "ai")

        # 🔥 GỌI ĐÚNG 1 LẦN DUY NHẤT
        files, all_code = tao_file(
            ds_bai,
            model_var.get(),
            lambda x: add_chat(x, "ai"),
            folder   # 🔥 QUAN TRỌNG
        )

        # hiển thị file đã tạo
        for f in files:
            add_chat(f"✔ Đã tạo file: {f}", "ai")

        add_chat(all_code, "code")

        last_code = all_code

        # push github
        if files:
            push_github(files, lambda x: add_chat(x, "ai"))

        status.config(text="✅ Hoàn thành", fg="#22c55e")

    except Exception as e:
        add_chat("❌ Lỗi Auto: " + str(e), "ai")
        status.config(text="Lỗi", fg="red")

    entry.delete(0, tk.END)

# ================== LƯU / COPY / XÓA ==================
def save_code():
    if not last_code:
        messagebox.showwarning("Thông báo", "Chưa có code!")
        return

    path = filedialog.asksaveasfilename(defaultextension=".py")
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(last_code)

def copy_code():
    if last_code:
        root.clipboard_clear()
        root.clipboard_append(last_code)
        messagebox.showinfo("Thông báo", "Đã copy!")

def clear_history():
    if messagebox.askyesno("Xác nhận", "Xóa lịch sử?"):
        open(HISTORY_FILE, "w").close()
        chat_box.config(state="normal")
        chat_box.delete("1.0", tk.END)
        chat_box.config(state="disabled")

# ================== INPUT ==================
input_frame = tk.Frame(root, bg="#0f172a")
input_frame.pack(fill="x")

entry = tk.Entry(input_frame,
                 bg="#1e293b",
                 fg="white",
                 font=FONT)

entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

# ENTER gửi
entry.bind("<Return>", lambda event: send_chat())

# SHIFT + ENTER auto
entry.bind("<Shift-Return>", lambda event: auto_bai())

# ===== tạo nút =====
def tao_nut(text, cmd, color):
    return tk.Button(input_frame,
                     text=text,
                     command=cmd,
                     bg=color,
                     fg="white",
                     font=FONT,
                     relief="flat",
                     padx=10)

tao_nut("Gửi", send_chat, "#22c55e").pack(side="right", padx=5)
tao_nut("Auto bài tập", auto_bai, "#f59e0b").pack(side="right", padx=5)
tao_nut("Lưu", save_code, "#a855f7").pack(side="right", padx=5)
tao_nut("Copy", copy_code, "#06b6d4").pack(side="right", padx=5)
tao_nut("Xóa", clear_history, "#ef4444").pack(side="right", padx=5)

# ================== STATUS ==================
status = tk.Label(root,
                  text="Sẵn sàng",
                  fg="#22c55e",
                  bg="#0f172a")

status.pack()

# load lịch sử
load_history()

# chạy app
root.mainloop()