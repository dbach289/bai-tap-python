# ================== BAI_HANDLER ==================
import re
import os
import unicodedata
from ai_handler import ask_ai

# ================== TÁCH BÀI ==================
def tach_bai(text):
    text = text.strip()

    # 🔥 FIX UNICODE
    text = unicodedata.normalize("NFC", text)
    text = text.replace("Bài", "Bài").replace("bài", "bài")
    text = re.sub(r"\bbai\b", "bài", text, flags=re.IGNORECASE)

    chuong_match = re.search(r"ch(ươ|u)ng\s*(\d+)", text, re.IGNORECASE)
    chuong = chuong_match.group(2) if chuong_match else "1"

    ds = []

    pattern = r"(bài\s*\d+[:\.]?.*?)(?=bài\s*\d+[:\.]?|$)"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

    if matches:
        for m in matches:
            so_match = re.search(r"\d+", m)
            bai = so_match.group()

            ds.append({
                "chuong": chuong,
                "bai": bai,
                "noi_dung": m.strip()
            })
        return ds

    return [{
        "chuong": chuong,
        "bai": "1",
        "noi_dung": text
    }]

# ================== TẠO CODE ==================
def tao_code(noi_dung, model):
    return ask_ai(noi_dung, model)

# ================== TẠO FILE ==================
def tao_file(ds_bai, model, log_func, save_root):
    files = []
    all_code = ""

    os.makedirs(save_root, exist_ok=True)

    for item in ds_bai:
        try:
            bai = item["bai"]
            noi_dung = item["noi_dung"]

            log_func(f"⏳ Đang tạo code Bài {bai}...")

            code = tao_code(noi_dung, model)

            if not code:
                log_func(f"❌ AI không trả code cho Bài {bai}")
                continue

            file_path = os.path.join(save_root, f"Bai{bai}.py")

            count = 1
            while os.path.exists(file_path):
                file_path = os.path.join(save_root, f"Bai{bai}_{count}.py")
                count += 1

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# ===== Bài {bai} =====\n")
                f.write(code)

            log_func(f"📄 {file_path}")

            files.append(file_path)
            all_code += f"\n# ===== Bài {bai} =====\n{code}\n"

        except Exception as e:
            log_func(f"❌ Lỗi Bài {item.get('bai', '?')}: {str(e)}")

    return files, all_code