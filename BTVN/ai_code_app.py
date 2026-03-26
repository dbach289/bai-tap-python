import tkinter as tk
from tkinter import messagebox, filedialog
from groq import Groq
import time
import os

# ================== KHỞI TẠO API ==================

client = Groq(api_key="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")

# ================== CẤU HÌNH ==================
DELAY = 2                     # Thời gian chờ giữa các lần gọi API (tránh spam)
last_call = 0                # Thời điểm gọi API gần nhất
HISTORY_FILE = "chat_history.txt"  # File lưu lịch sử chat
last_code = ""               # Lưu đoạn code gần nhất để save/copy

# ================== TẠO CỬA SỔ CHÍNH ==================
root = tk.Tk()
root.title("Ứng dụng Chat AI hỗ trợ code Python")
root.geometry("1000x750")
root.configure(bg="#0f172a")  # Màu nền tối

FONT = ("Segoe UI", 11)

# ================== CHỌN MODEL ==================
model_var = tk.StringVar(value="llama-3.3-70b-versatile")

# Thông tin mô tả model
MODEL_INFO = {
    "llama-3.1-8b-instant": "Nhanh | Độ chính xác trung bình",
    "llama-3.3-70b-versatile": "Chậm hơn | Rất thông minh"
}

# ================== HEADER ==================
header = tk.Frame(root, bg="#020617", height=50)
header.pack(fill="x")

tk.Label(header,
         text="AI HỖ TRỢ LẬP TRÌNH",
         fg="#22c55e",
         bg="#020617",
         font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

# ================== KHU VỰC CHỌN MODEL ==================
model_frame = tk.Frame(header, bg="#020617")
model_frame.pack(side="right", padx=10)

tk.Label(model_frame,
         text="Chọn Model:",
         fg="white",
         bg="#020617",
         font=FONT).pack(side="left")

# Dropdown chọn model
model_menu = tk.OptionMenu(model_frame,
                           model_var,
                           "llama-3.3-70b-versatile",
                           "llama-3.1-8b-instant")

model_menu.config(bg="#1e293b",
                  fg="white",
                  font=FONT,
                  width=25,
                  relief="flat")

model_menu.pack(side="left", padx=5)

# Hiển thị mô tả model
model_info = tk.Label(header,
                      text=MODEL_INFO[model_var.get()],
                      fg="#94a3b8",
                      bg="#020617",
                      font=("Segoe UI", 9))

model_info.pack(side="right", padx=10)

# Khi đổi model thì cập nhật mô tả
def update_model(*args):
    model_info.config(text=MODEL_INFO[model_var.get()])

model_var.trace("w", update_model)

# ================== KHUNG HIỂN THỊ CHAT ==================
chat_frame = tk.Frame(root, bg="#0f172a")
chat_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side="right", fill="y")

chat_box = tk.Text(chat_frame,
                   bg="#020617",
                   fg="#e2e8f0",
                   font=FONT,
                   wrap="word",
                   insertbackground="white",
                   yscrollcommand=scrollbar.set)

chat_box.pack(fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=chat_box.yview)

chat_box.config(state="disabled")  # Không cho sửa nội dung

# ================== ĐỊNH DẠNG MÀU ==================
chat_box.tag_config("user", foreground="#38bdf8")     # Người dùng
chat_box.tag_config("ai", foreground="#22c55e")       # AI
chat_box.tag_config("code", foreground="#facc15")     # Code
chat_box.tag_config("explain", foreground="#c084fc")  # Giải thích

# ================== HÀM THÊM NỘI DUNG CHAT ==================
def add_chat(text, tag=None):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, text + "\n\n", tag)
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

    # Lưu vào file lịch sử
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n\n")

# ================== LOAD LỊCH SỬ ==================
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, f.read())
            chat_box.config(state="disabled")

# ================== GỌI AI ==================
def ask_ai(prompt):
    global last_call

    # Nếu gọi quá nhanh thì chờ
    if time.time() - last_call < DELAY:
        time.sleep(DELAY)

    status.config(text="AI đang xử lý...", fg="yellow")
    root.update()

    try:
        res = client.chat.completions.create(
            model=model_var.get(),
            messages=[
                {"role": "system", "content": "Bạn là AI hỗ trợ lập trình Python."},
                {"role": "user", "content": prompt}
            ]
        )

        last_call = time.time()
        status.config(text="Hoàn thành!", fg="#22c55e")

        return res.choices[0].message.content

    except Exception as e:
        status.config(text="Lỗi API!", fg="red")
        return str(e)

# ================== TÁCH CODE VÀ GIẢI THÍCH ==================
def parse_result(result):
    if "EXPLAIN:" in result:
        parts = result.split("EXPLAIN:")
        code = parts[0].replace("CODE:", "").strip()
        explain = parts[1].strip()
    else:
        code = result
        explain = "Không có giải thích."

    return code, explain

# ================== GỬI CÂU HỎI ==================
def send():
    global last_code

    text = entry.get().strip()
    if not text:
        return

    add_chat("Bạn: " + text, "user")
    entry.delete(0, tk.END)

    prompt = f"""
Yêu cầu: {text}

Trả lời bằng tiếng Việt

CODE:
<code>

EXPLAIN:
<giải thích>
"""

    result = ask_ai(prompt)

    code, explain = parse_result(result)
    last_code = code

    add_chat(f"AI ({model_var.get()}):", "ai")
    add_chat("CODE:\n" + code, "code")
    add_chat("GIẢI THÍCH:\n" + explain, "explain")

# ================== LƯU CODE ==================
def save_code():
    if not last_code:
        messagebox.showwarning("Thông báo", "Chưa có code để lưu!")
        return

    path = filedialog.asksaveasfilename(
        title="Chọn nơi lưu file",
        defaultextension=".py"
    )

    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(last_code)

# ================== COPY CODE ==================
def copy_code():
    if last_code:
        root.clipboard_clear()
        root.clipboard_append(last_code)
        messagebox.showinfo("Thông báo", "Đã copy code!")

# ================== XÓA LỊCH SỬ ==================
def clear_history():
    if messagebox.askyesno("Xác nhận", "Bạn có muốn xóa lịch sử không?"):
        open(HISTORY_FILE, "w").close()
        chat_box.config(state="normal")
        chat_box.delete("1.0", tk.END)
        chat_box.config(state="disabled")

# ================== KHUNG NHẬP ==================
input_frame = tk.Frame(root, bg="#0f172a")
input_frame.pack(fill="x")

entry = tk.Entry(input_frame,
                 bg="#1e293b",
                 fg="white",
                 insertbackground="white",
                 font=FONT)

entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

# Hàm tạo nút
def tao_nut(text, cmd, color):
    return tk.Button(input_frame,
                     text=text,
                     command=cmd,
                     bg=color,
                     fg="white",
                     font=FONT,
                     relief="flat",
                     padx=10)

tao_nut("Gửi", send, "#22c55e").pack(side="right", padx=5)
tao_nut("Lưu", save_code, "#a855f7").pack(side="right", padx=5)
tao_nut("Copy", copy_code, "#06b6d4").pack(side="right", padx=5)
tao_nut("Xóa", clear_history, "#ef4444").pack(side="right", padx=5)

# ================== TRẠNG THÁI ==================
status = tk.Label(root,
                  text="Sẵn sàng",
                  fg="#22c55e",
                  bg="#0f172a",
                  font=("Segoe UI", 10))

status.pack()

# Load lịch sử khi mở app
load_history()

# Chạy chương trình
root.mainloop()