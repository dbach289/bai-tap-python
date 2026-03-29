# ================== AI_HANDLER ==================
# File xử lý gọi AI (đã fix full)

from groq import Groq
import time
import os
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# ❗ Kiểm tra key
if not api_key:
    raise ValueError("❌ Không tìm thấy GROQ_API_KEY trong file .env")

# ===== TẠO CLIENT (FIX LỖI CHÍNH) =====
client = Groq(api_key=api_key)

# ===== CONFIG =====
DELAY = 2
last_call = 0


# ================== CLEAN CODE ==================
def clean_code(text):
    """
    Xóa ```python ... ``` nếu AI trả về
    """
    if "```" in text:
        lines = text.split("\n")
        cleaned = []

        for line in lines:
            if line.strip().startswith("```"):
                continue
            cleaned.append(line)

        return "\n".join(cleaned).strip()

    return text.strip()


# ================== ASK AI ==================
def ask_ai(prompt, model="llama3-70b-8192"):
    global last_call

    # ⏳ chống spam API
    wait_time = DELAY - (time.time() - last_call)
    if wait_time > 0:
        time.sleep(wait_time)

    try:
        full_prompt = f"""
Bạn là AI chuyên viết code Python.

Yêu cầu:
- Chỉ trả về code Python
- Không giải thích
- Có chú thích tiếng Việt
- Code chạy được 100%
- Nếu đề bài ngắn, tự suy luận để hoàn chỉnh

Bài toán:
{prompt}
"""

        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Bạn là AI code Python chuyên nghiệp"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.2
        )

        last_call = time.time()

        content = res.choices[0].message.content

        if not content:
            return "# ❌ AI không trả về dữ liệu"

        return clean_code(content)

    except Exception as e:
        return f"# ❌ Lỗi AI: {str(e)}"