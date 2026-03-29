# ================== GITHUB_HANDLER ==================
# Auto push GitHub FULL FIX (không lỗi vặt)

import subprocess
import os

def run_git(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def push_github(files, log_func):
    try:
        # ===== CHO PHÉP 1 FILE HOẶC LIST =====
        if isinstance(files, str):
            files = [files]

        log_func("🚀 Đang push GitHub...")

        # ===== INIT REPO NẾU CHƯA CÓ =====
        if not os.path.exists(".git"):
            log_func("⚠️ Chưa có repo → đang init...")
            run_git(["git", "init"])
            run_git(["git", "branch", "-M", "main"])

        # ===== ADD FILE =====
        run_git(["git", "add", "."])

        # ===== COMMIT =====
        file_names = [os.path.basename(f) for f in files]
        commit_msg = "Update: " + ", ".join(file_names)

        commit = run_git(["git", "commit", "-m", commit_msg])
        if "nothing to commit" in commit.stdout.lower():
            log_func("ℹ️ Không có thay đổi mới")
        else:
            log_func("✔ Đã commit")

        # ===== KIỂM TRA REMOTE =====
        remote = run_git(["git", "remote", "-v"])
        if "origin" not in remote.stdout:
            log_func("❌ Chưa có remote origin")
            log_func("👉 Chạy: git remote add origin <URL>")
            return

        # ===== PULL TRƯỚC (FIX FETCH FIRST) =====
        pull = run_git(["git", "pull", "origin", "main", "--rebase"])
        if pull.returncode != 0:
            log_func("⚠️ Pull có cảnh báo (có thể conflict nhẹ)")

        # ===== PUSH =====
        push = run_git(["git", "push", "origin", "main"])

        if push.returncode != 0:
            log_func("⚠️ Push bị reject → thử force push...")

            force = run_git(["git", "push", "-f", "origin", "main"])
            if force.returncode == 0:
                log_func("🔥 Force push thành công")
            else:
                log_func(f"❌ Force push lỗi:\n{force.stderr}")
                return
        else:
            log_func("✅ Push thành công")

    except Exception as e:
        log_func(f"❌ Lỗi hệ thống: {str(e)}")