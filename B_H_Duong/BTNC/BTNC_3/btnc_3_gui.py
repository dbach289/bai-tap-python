import os
import ast
import math
import re
import tokenize
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter
from io import StringIO
from typing import Iterable, List, Tuple
from fpdf import FPDF

# Thu muc tool: .../B_H_Duong/BTNC/BTNC_3
# BTNC_AI_1 / BTNC_AI_2 nam trong .../B_H_Duong/BTNC (cung cap voi BTNC_3), khong nam trong BTNC_3.
_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_BTNC_DIR = os.path.dirname(_APP_DIR)

PYTHON_EXTENSIONS = {".py"}
REPORT_EXTENSIONS = {".txt", ".md", ".rst"}


def collect_files(root_dir: str, allowed_extensions: Iterable[str]) -> List[str]:
    matched = []
    for current_root, _, files in os.walk(root_dir):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in allowed_extensions:
                matched.append(os.path.join(current_root, name))
    return matched


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def normalize_code_tokens(code: str) -> List[str]:
    tokens = []
    stream = StringIO(code).readline
    try:
        for tok in tokenize.generate_tokens(stream):
            tok_type = tok.type
            tok_val = tok.string
            if tok_type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                continue
            if tok_type == tokenize.STRING and tok.start[0] == 1:
                continue
            if tok_type == tokenize.NAME:
                if tok_val in {"def", "class", "for", "while", "if", "elif", "else", "return", "try", "except", "with", "import", "from"}:
                    tokens.append(tok_val)
                else:
                    tokens.append("IDENT")
            elif tok_type == tokenize.NUMBER:
                tokens.append("NUMBER")
            elif tok_type == tokenize.STRING:
                tokens.append("STRING")
            else:
                tokens.append(tok_val)
    except tokenize.TokenError:
        tokens = re.findall(r"[A-Za-z_]+|\d+|[^\s]", code)
    return tokens


def shingles(tokens: List[str], k: int = 5) -> set:
    if len(tokens) < k:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i:i + k]) for i in range(len(tokens) - k + 1)}


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    intersection = len(a.intersection(b))
    union = len(a.union(b))
    return intersection / union if union else 0.0


def extract_ast_features(code: str) -> Counter:
    features = Counter()
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return features
    for node in ast.walk(tree):
        node_name = type(node).__name__
        features[f"NODE_{node_name}"] += 1
        if isinstance(node, ast.Import):
            for alias in node.names:
                features[f"IMPORT_{alias.name.split('.')[0]}"] += 1
        elif isinstance(node, ast.ImportFrom) and node.module:
            features[f"IMPORT_{node.module.split('.')[0]}"] += 1
        elif isinstance(node, ast.FunctionDef):
            features["FUNC_COUNT"] += 1
            features[f"FUNC_ARGS_{len(node.args.args)}"] += 1
        elif isinstance(node, ast.ClassDef):
            features["CLASS_COUNT"] += 1
    return features


def cosine_similarity(c1: Counter, c2: Counter) -> float:
    keys = set(c1.keys()).union(c2.keys())
    if not keys:
        return 1.0
    dot = sum(c1[k] * c2[k] for k in keys)
    norm1 = math.sqrt(sum(c1[k] ** 2 for k in keys))
    norm2 = math.sqrt(sum(c2[k] ** 2 for k in keys))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def normalize_text(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\u00c0-\u1ef9\s]", " ", text)
    words = [w for w in text.split() if len(w) > 1]
    return words


def star_rating(percent: float) -> str:
    stars = max(1, min(10, round(percent / 10)))
    return "*" * stars


def risk_level(percent: float) -> str:
    if percent >= 80:
        return "RAT CAO"
    if percent >= 60:
        return "CAO"
    if percent >= 40:
        return "TRUNG BINH"
    if percent >= 20:
        return "THAP"
    return "RAT THAP"


def compare_code_similarity(dir1: str, dir2: str) -> Tuple[float, int, int]:
    files1 = collect_files(dir1, PYTHON_EXTENSIONS)
    files2 = collect_files(dir2, PYTHON_EXTENSIONS)
    all_tokens1: List[str] = []
    for path in files1:
        all_tokens1.extend(normalize_code_tokens(read_text(path)))
    all_tokens2: List[str] = []
    for path in files2:
        all_tokens2.extend(normalize_code_tokens(read_text(path)))
    score = jaccard_similarity(shingles(all_tokens1), shingles(all_tokens2))
    return score * 100, len(files1), len(files2)


def compare_file_pairs_code_similarity(dir1: str, dir2: str, top_n: int = 5) -> List[Tuple[str, str, float]]:
    files1 = collect_files(dir1, PYTHON_EXTENSIONS)
    files2 = collect_files(dir2, PYTHON_EXTENSIONS)
    token_map_1 = {p: normalize_code_tokens(read_text(p)) for p in files1}
    token_map_2 = {p: normalize_code_tokens(read_text(p)) for p in files2}
    results: List[Tuple[str, str, float]] = []
    for f1, t1 in token_map_1.items():
        s1 = shingles(t1)
        for f2, t2 in token_map_2.items():
            sim = jaccard_similarity(s1, shingles(t2)) * 100
            results.append((f1, f2, sim))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_n]


def compare_approach_similarity(dir1: str, dir2: str) -> float:
    files1 = collect_files(dir1, PYTHON_EXTENSIONS)
    files2 = collect_files(dir2, PYTHON_EXTENSIONS)
    features1 = Counter()
    for path in files1:
        features1.update(extract_ast_features(read_text(path)))
    features2 = Counter()
    for path in files2:
        features2.update(extract_ast_features(read_text(path)))
    return cosine_similarity(features1, features2) * 100


def compare_report_similarity(dir1: str, dir2: str) -> Tuple[float, int, int]:
    reports1 = collect_files(dir1, REPORT_EXTENSIONS)
    reports2 = collect_files(dir2, REPORT_EXTENSIONS)
    words1 = []
    for path in reports1:
        words1.extend(normalize_text(read_text(path)))
    words2 = []
    for path in reports2:
        words2.extend(normalize_text(read_text(path)))
    score = jaccard_similarity(set(words1), set(words2))
    return score * 100, len(reports1), len(reports2)


def compare_two_files(file1: str, file2: str) -> Tuple[float, float, float]:
    text1 = read_text(file1)
    text2 = read_text(file2)
    code_percent = jaccard_similarity(
        shingles(normalize_code_tokens(text1)),
        shingles(normalize_code_tokens(text2)),
    ) * 100
    approach_percent = cosine_similarity(
        extract_ast_features(text1),
        extract_ast_features(text2),
    ) * 100
    report_percent = jaccard_similarity(
        set(normalize_text(text1)),
        set(normalize_text(text2)),
    ) * 100
    return code_percent, approach_percent, report_percent


def build_report_text(
    dir1: str,
    dir2: str,
    code_percent: float,
    py_count_1: int,
    py_count_2: int,
    approach_percent: float,
    report_percent: float,
    report_count_1: int,
    report_count_2: int,
    top_pairs: List[Tuple[str, str, float]],
) -> str:
    lines = [
        "=== KET QUA DANH GIA TRUNG LAP ===",
        f"Thu muc 1: {dir1}",
        f"Thu muc 2: {dir2}",
        "",
        f"1) Trung lap CODE (%): {code_percent:.2f}% | Muc do: {risk_level(code_percent)}",
        f"   - So file Python: {py_count_1} vs {py_count_2}",
        "",
        f"2) Trung lap CACH GIAI QUYET / CACH CODE (%): {approach_percent:.2f}% | Muc do: {risk_level(approach_percent)}",
        "   - Danh gia theo AST: cau truc node, import, ham, class, so luong tham so...",
        "",
        f"3) Trung lap BAO CAO / TIEU LUAN (%): {report_percent:.2f}% | Muc do: {risk_level(report_percent)}",
        f"   - So file van ban: {report_count_1} vs {report_count_2}",
        f"   - Muc canh bao sao: {star_rating(report_percent)}",
        "",
        "4) TOP CAP FILE PYTHON GIONG NHAU NHAT:",
    ]
    if not top_pairs:
        lines.append("   - Khong tim thay cap file Python de so sanh.")
    else:
        for i, (f1, f2, sim) in enumerate(top_pairs, start=1):
            lines.append(f"   {i}. {sim:.2f}%")
            lines.append(f"      - File 1: {f1}")
            lines.append(f"      - File 2: {f2}")
    lines.extend(
        [
            "",
            "Luu y: ket qua mang tinh tham khao tu dong, can ket hop danh gia thu cong de ket luan hoc thuat.",
        ]
    )
    return "\n".join(lines)


def _pdf_split_line_to_page_width(pdf: FPDF, text: str) -> List[str]:
    """Cat text thanh cac doan vua be ngang hieu dung (epw); tranh loi 'Not enough horizontal space'."""
    # Tru bot vai mm de khoi lech voi bo xuong dong noi bo cua fpdf2 (lam tron).
    max_w = float(pdf.epw) * 0.98
    if not text:
        return []
    if pdf.get_string_width(text) <= max_w:
        return [text]
    chunks: List[str] = []
    buf = ""
    for ch in text:
        cand = buf + ch
        if pdf.get_string_width(cand) <= max_w:
            buf = cand
        else:
            if buf:
                chunks.append(buf)
            buf = ch
            if pdf.get_string_width(buf) > max_w:
                chunks.append(buf)
                buf = ""
    if buf:
        chunks.append(buf)
    return chunks


def _pdf_write_wrapped_body(pdf: FPDF, body: str, font_ok: bool, line_h: float = 7) -> None:
    """Ghi noi dung nhieu dong; path dai khong co khoang trang van xuong dong duoc."""
    for raw in body.splitlines():
        safe = raw if font_ok else raw.encode("latin-1", "replace").decode("latin-1")
        safe = safe.replace("\t", "    ")
        if not safe.strip():
            pdf.ln(line_h)
            continue
        for part in _pdf_split_line_to_page_width(pdf, safe):
            if not part:
                continue
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.epw, line_h, part)


class SimilarityApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("BTNC_3 | B_H_Duong > BTNC > BTNC_3")
        self.root.geometry("1020x920")
        self.root.minsize(900, 700)

        self.mode = tk.StringVar(value="folder")
        self.path1 = tk.StringVar()
        self.path2 = tk.StringVar()
        self.output_path = tk.StringVar(value=os.path.join(_APP_DIR, "btnc_3_gui_report.txt"))
        self.top_n = tk.IntVar(value=5)
        self.latest_report_text = ""
        self.latest_scores = {"code": 0.0, "approach": 0.0, "report": 0.0}

        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.LabelFrame(self.root, text="Vi tri bai (dung cau truc nay)")
        header.pack(fill="x", padx=10, pady=(10, 0))
        ttk.Label(
            header,
            text="B_H_Duong  >  BTNC  >  BTNC_3",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=8, pady=(6, 2))
        ttk.Label(
            header,
            text=(
                f"Duong dan thu muc BTNC_3 (file chuong trinh):\n{_APP_DIR}\n\n"
                f"Duong dan thu muc BTNC (BTNC_AI_1, BTNC_AI_2):\n{_BTNC_DIR}"
            ),
            wraplength=920,
            justify="left",
        ).pack(anchor="w", padx=8, pady=(0, 8))

        mode_frame = ttk.LabelFrame(self.root, text="Che do so sanh")
        mode_frame.pack(fill="x", padx=10, pady=8)
        ttk.Radiobutton(
            mode_frame,
            text="So sanh 2 thu muc san pham",
            variable=self.mode,
            value="folder",
            command=self._on_mode_change,
        ).pack(side="left", padx=10, pady=8)
        ttk.Radiobutton(
            mode_frame,
            text="So sanh truc tiep 2 file",
            variable=self.mode,
            value="file",
            command=self._on_mode_change,
        ).pack(side="left", padx=10, pady=8)

        path_frame = ttk.LabelFrame(self.root, text="Chon du lieu dau vao")
        path_frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(path_frame, text="Doi tuong 1:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        ttk.Entry(path_frame, textvariable=self.path1, width=90).grid(row=0, column=1, padx=8, pady=8, sticky="we")
        ttk.Button(path_frame, text="Chon...", command=lambda: self._pick_path(self.path1)).grid(
            row=0, column=2, padx=8, pady=8
        )

        ttk.Label(path_frame, text="Doi tuong 2:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        ttk.Entry(path_frame, textvariable=self.path2, width=90).grid(row=1, column=1, padx=8, pady=8, sticky="we")
        ttk.Button(path_frame, text="Chon...", command=lambda: self._pick_path(self.path2)).grid(
            row=1, column=2, padx=8, pady=8
        )

        self.top_label = ttk.Label(path_frame, text="Top cap file (chi cho thu muc):")
        self.top_label.grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.top_spinbox = ttk.Spinbox(path_frame, from_=1, to=100, textvariable=self.top_n, width=8)
        self.top_spinbox.grid(
            row=2, column=1, padx=8, pady=8, sticky="w"
        )

        ttk.Label(path_frame, text="File report txt:").grid(row=3, column=0, padx=8, pady=8, sticky="w")
        ttk.Entry(path_frame, textvariable=self.output_path, width=90).grid(row=3, column=1, padx=8, pady=8, sticky="we")
        ttk.Button(path_frame, text="Luu vao...", command=self._pick_output).grid(row=3, column=2, padx=8, pady=8)
        ttk.Button(
            path_frame,
            text="Dien san: BTNC_AI_1 vs BTNC_AI_2 (trong thu muc BTNC)",
            command=self._fill_demo_folders,
        ).grid(row=4, column=0, columnspan=3, padx=8, pady=8, sticky="w")
        path_frame.columnconfigure(1, weight=1)

        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=4)
        ttk.Button(action_frame, text="So sanh ngay", command=self._run_compare).pack(side="left", padx=4)
        ttk.Button(action_frame, text="Xuat PDF", command=self._export_pdf).pack(side="left", padx=4)
        ttk.Button(action_frame, text="Xoa ket qua", command=self._clear_result).pack(side="left", padx=4)

        chart_frame = ttk.LabelFrame(self.root, text="Bieu do % trung lap (xem nhanh ket qua)")
        chart_frame.pack(fill="x", padx=10, pady=(4, 6))
        self.chart_canvas = tk.Canvas(chart_frame, height=440, bg="#0f1923", highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=10, pady=10)
        self._draw_chart(0.0, 0.0, 0.0)
        self.chart_canvas.bind("<Configure>", self._on_chart_resize)

        self.quick_result = ttk.Label(
            self.root,
            text="San sang so sanh. Chon duong dan va bam 'So sanh ngay'.",
            foreground="#4fc3f7",
            font=("Segoe UI", 11),
        )
        self.quick_result.pack(fill="x", padx=12, pady=(4, 6))

        result_frame = ttk.LabelFrame(self.root, text="Ket qua chi tiet")
        result_frame.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        self.result_text = tk.Text(result_frame, wrap="word", font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True, padx=8, pady=8)
        self._on_mode_change()

    def _on_chart_resize(self, _event: object = None) -> None:
        """Ve lai bieu do khi thay doi kich thuoc cua so (canvas rong hon)."""
        s = self.latest_scores
        self._draw_chart(s["code"], s["approach"], s["report"])

    def _fill_demo_folders(self) -> None:
        """Dien nhanh 2 thu muc demo trong thu muc BTNC (cung cap voi BTNC_3)."""
        self.mode.set("folder")
        self._on_mode_change()
        d1 = os.path.join(_BTNC_DIR, "BTNC_AI_1")
        d2 = os.path.join(_BTNC_DIR, "BTNC_AI_2")
        if os.path.isdir(d1) and os.path.isdir(d2):
            self.path1.set(d1)
            self.path2.set(d2)
            messagebox.showinfo(
                "OK",
                "Da dien san 2 thu muc BTNC_AI_1 va BTNC_AI_2 trong thu muc BTNC.",
            )
        else:
            messagebox.showwarning(
                "Khong tim thay",
                "Trong thu muc BTNC can co 2 thu muc: BTNC_AI_1 va BTNC_AI_2.\n"
                f"Thu muc BTNC: {_BTNC_DIR}",
            )

    def _on_mode_change(self) -> None:
        # Mode file: khoa top_n de tranh nguoi dung nham lan.
        if self.mode.get() == "file":
            self.top_spinbox.configure(state="disabled")
            self.top_label.configure(foreground="#888888")
        else:
            self.top_spinbox.configure(state="normal")
            self.top_label.configure(foreground="#000000")

    def _pick_path(self, target_var: tk.StringVar) -> None:
        if self.mode.get() == "folder":
            picked = filedialog.askdirectory(title="Chon thu muc")
        else:
            picked = filedialog.askopenfilename(title="Chon file")
        if picked:
            target_var.set(picked)

    def _pick_output(self) -> None:
        output = filedialog.asksaveasfilename(
            title="Chon file report text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if output:
            self.output_path.set(output)

    def _clear_result(self) -> None:
        self.result_text.delete("1.0", "end")
        self.quick_result.config(text="Da xoa ket qua.")
        self.quick_result.config(foreground="#4fc3f7")
        self.latest_report_text = ""
        self.latest_scores = {"code": 0.0, "approach": 0.0, "report": 0.0}
        self._draw_chart(0.0, 0.0, 0.0)

    def _risk_color(self, level: str) -> str:
        if level in {"RAT CAO", "CAO"}:
            return "#c62828"
        if level == "TRUNG BINH":
            return "#ef6c00"
        return "#2e7d32"

    def _draw_chart(self, code: float, approach: float, report: float) -> None:
        canvas = self.chart_canvas
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 520)
        height = int(canvas.cget("height"))
        canvas.delete("all")

        if width < 10 or height < 10:
            return

        font_axis = ("Segoe UI", 11)
        font_legend = ("Segoe UI", 12, "bold")
        font_pct = ("Segoe UI", 18, "bold")
        font_bar_name = ("Segoe UI", 13, "bold")

        # ---- Nền ----
        canvas.create_rectangle(0, 0, width, height, fill="#0f1923", outline="")
        canvas.create_rectangle(0, height // 2, width, height, fill="#162030", outline="")

        labels = [
            ("CODE", code, ("#00c6ff", "#0072ff"), ("#00c6ff", "#0072ff")),
            ("CÁCH CODE", approach, ("#a855f7", "#ec4899"), ("#a855f7", "#ec4899")),
            ("BÁO CÁO", report, ("#10b981", "#34d399"), ("#10b981", "#34d399")),
        ]

        n = len(labels)
        pad_left = 56
        pad_right = 28
        avail = width - pad_left - pad_right
        gap = 64
        bar_w = 168
        bar_pad = 12
        legend_y = 14
        swatch_w, swatch_h = 56, 26
        leg_gap = 36
        leg_text = ["CODE", "CÁCH CODE", "BÁO CÁO"]
        block_w = swatch_w + 14 + 118
        total_leg = n * block_w + (n - 1) * leg_gap
        leg_x0 = max(pad_left, (width - total_leg) // 2)

        for i, leg in enumerate(leg_text):
            c1 = labels[i][2][0]
            bx = leg_x0 + i * (block_w + leg_gap)
            canvas.create_rectangle(
                bx, legend_y, bx + swatch_w, legend_y + swatch_h,
                fill=c1, outline="#5a7a9a", width=1,
            )
            canvas.create_text(
                bx + swatch_w + 10,
                legend_y + swatch_h // 2,
                text=leg,
                font=font_legend,
                fill="#d8e4f0",
                anchor="w",
            )

        top_y = legend_y + swatch_h + 22
        base_y = height - 44
        max_h = base_y - top_y

        # ---- Lưới ngang + số trục Y ----
        for mark in [0, 25, 50, 75, 100]:
            y = base_y - max_h * mark / 100.0
            canvas.create_line(pad_left, y, width - pad_right, y, fill="#2a3f58", width=1)
            canvas.create_text(
                pad_left - 10,
                y,
                text=str(mark),
                font=font_axis,
                fill="#a8b8c8",
                anchor="e",
            )

        canvas.create_line(pad_left, base_y, width - pad_right, base_y, fill="#4a6a8a", width=2)

        total_bar_area = n * bar_w + (n - 1) * gap
        start_x = pad_left + max(0, (avail - total_bar_area) // 2)

        for i, (name, value, (c1, c2), (gc1, gc2)) in enumerate(labels):
            x1 = start_x + i * (bar_w + gap)
            x2 = x1 + bar_w
            h = max_h * max(0.0, min(100.0, value)) / 100.0
            y1 = base_y - h
            clip_top = y1 < top_y

            segs = 24
            for s in range(segs):
                ratio_f = s / segs
                ratio_t = (s + 1) / segs
                sy1 = y1 + h * ratio_f
                sy2 = min(y1 + h * ratio_t, base_y)
                frac = s / segs
                r = int(int(c1[1:3], 16) * (1 - frac) + int(c2[1:3], 16) * frac)
                g = int(int(c1[3:5], 16) * (1 - frac) + int(c2[3:5], 16) * frac)
                b = int(int(c1[5:7], 16) * (1 - frac) + int(c2[5:7], 16) * frac)
                seg_color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_rectangle(
                    x1 + bar_pad, sy1, x2 - bar_pad, sy2,
                    fill=seg_color, outline="",
                )

            if clip_top:
                canvas.create_rectangle(x1 + bar_pad, top_y, x2 - bar_pad, y1, fill="#ffffff", outline="")

            canvas.create_rectangle(
                x1 + bar_pad - 2, y1 - 2,
                x2 - bar_pad + 2, base_y + 2,
                fill="", outline=gc1, width=2,
            )

            lbl_pct = f"{value:.1f}%"
            lbl_color = "#ff6b6b" if value >= 80 else ("#ffd93d" if value >= 40 else "#6bcb77")
            pct_y = max(top_y + 8, y1 - 22)
            canvas.create_text((x1 + x2) / 2, pct_y, text=lbl_pct, font=font_pct, fill=lbl_color)

            canvas.create_text(
                (x1 + x2) / 2,
                base_y + 20,
                text=name,
                font=font_bar_name,
                fill="#b0c4d4",
            )

    def _run_compare(self) -> None:
        p1 = self.path1.get().strip().strip('"')
        p2 = self.path2.get().strip().strip('"')
        out = self.output_path.get().strip().strip('"')

        if not p1 or not p2:
            messagebox.showwarning("Thieu du lieu", "Ban can chon day du 2 duong dan.")
            return

        try:
            if self.mode.get() == "folder":
                if not os.path.isdir(p1) or not os.path.isdir(p2):
                    raise ValueError("Che do thu muc yeu cau 2 duong dan thu muc hop le.")

                code_percent, py_count_1, py_count_2 = compare_code_similarity(p1, p2)
                approach_percent = compare_approach_similarity(p1, p2)
                report_percent, report_count_1, report_count_2 = compare_report_similarity(p1, p2)
                top_pairs = compare_file_pairs_code_similarity(p1, p2, top_n=max(1, self.top_n.get()))

                report_text = build_report_text(
                    dir1=os.path.abspath(p1),
                    dir2=os.path.abspath(p2),
                    code_percent=code_percent,
                    py_count_1=py_count_1,
                    py_count_2=py_count_2,
                    approach_percent=approach_percent,
                    report_percent=report_percent,
                    report_count_1=report_count_1,
                    report_count_2=report_count_2,
                    top_pairs=top_pairs,
                )
                quick = (
                    f"CODE: {code_percent:.2f}% ({risk_level(code_percent)}) | "
                    f"CACH CODE: {approach_percent:.2f}% ({risk_level(approach_percent)}) | "
                    f"BAO CAO: {report_percent:.2f}% {star_rating(report_percent)}"
                )
            else:
                if not os.path.isfile(p1) or not os.path.isfile(p2):
                    raise ValueError("Che do file yeu cau 2 duong dan file hop le.")

                code_percent, approach_percent, report_percent = compare_two_files(p1, p2)
                report_text = "\n".join(
                    [
                        "=== KET QUA SO SANH 2 FILE ===",
                        f"File 1: {os.path.abspath(p1)}",
                        f"File 2: {os.path.abspath(p2)}",
                        "",
                        f"1) Trung lap CODE (%): {code_percent:.2f}% | Muc do: {risk_level(code_percent)}",
                        f"2) Trung lap CACH GIAI QUYET / CACH CODE (%): {approach_percent:.2f}% | Muc do: {risk_level(approach_percent)}",
                        f"3) Trung lap NOI DUNG VAN BAN (%): {report_percent:.2f}% | Muc do: {risk_level(report_percent)}",
                        f"   - Muc canh bao sao: {star_rating(report_percent)}",
                    ]
                )
                quick = (
                    f"CODE: {code_percent:.2f}% ({risk_level(code_percent)}) | "
                    f"CACH CODE: {approach_percent:.2f}% ({risk_level(approach_percent)}) | "
                    f"VAN BAN: {report_percent:.2f}% {star_rating(report_percent)}"
                )

            self.quick_result.config(text=quick)
            self.quick_result.config(foreground=self._risk_color(risk_level(max(code_percent, approach_percent, report_percent))))
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", report_text)
            self.latest_report_text = report_text
            self.latest_scores = {
                "code": code_percent,
                "approach": approach_percent,
                "report": report_percent,
            }
            self._draw_chart(code_percent, approach_percent, report_percent)

            if out:
                with open(out, "w", encoding="utf-8") as f:
                    f.write(report_text + "\n")
            messagebox.showinfo("Thanh cong", f"So sanh xong.\nDa luu report: {out}")

        except Exception as exc:
            messagebox.showerror("Loi", str(exc))

    def _export_pdf(self) -> None:
        if not self.latest_report_text.strip():
            messagebox.showwarning("Chua co du lieu", "Ban can bam 'So sanh ngay' truoc khi xuat PDF.")
            return

        pdf_path = filedialog.asksaveasfilename(
            title="Luu bao cao PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if not pdf_path:
            return

        try:
            pdf = FPDF()
            pdf.set_margins(12, 12, 12)
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=14)

            font_ok = False
            font_candidates = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/tahoma.ttf",
                "C:/Windows/Fonts/calibri.ttf",
            ]
            for font_path in font_candidates:
                if os.path.exists(font_path):
                    pdf.add_font("VN", "", font_path)
                    pdf.set_font("VN", size=11)
                    font_ok = True
                    break
            if not font_ok:
                pdf.set_font("Helvetica", size=11)

            title = "BAO CAO KIEM TRA TRUNG LAP - BTNC_3"
            pdf.cell(0, 8, title if font_ok else title.encode("latin-1", "replace").decode("latin-1"), ln=True)
            pdf.ln(2)
            _pdf_write_wrapped_body(pdf, self.latest_report_text, font_ok=font_ok, line_h=7)

            pdf.ln(2)
            pdf.set_font_size(10)
            if font_ok:
                pdf.set_font("VN", size=10)
            else:
                pdf.set_font("Helvetica", size=10)
            for row in (
                "Tong quan diem trung lap:",
                f"- Code: {self.latest_scores['code']:.2f}%",
                f"- Cach code: {self.latest_scores['approach']:.2f}%",
                f"- Bao cao/van ban: {self.latest_scores['report']:.2f}%",
            ):
                safe_row = row if font_ok else row.encode("latin-1", "replace").decode("latin-1")
                for chunk in _pdf_split_line_to_page_width(pdf, safe_row):
                    pdf.cell(0, 7, chunk, ln=True)

            pdf.output(pdf_path)
            messagebox.showinfo("Thanh cong", f"Da xuat PDF:\n{pdf_path}")
        except Exception as exc:
            messagebox.showerror("Loi xuat PDF", str(exc))


def main() -> None:
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    SimilarityApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
