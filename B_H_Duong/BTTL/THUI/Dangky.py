import re
import sqlite3
import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QButtonGroup,
    QHeaderView,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)

ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
HEADER_STRETCH = QHeaderView.ResizeMode.Stretch
MESSAGEBOX_YES = QMessageBox.StandardButton.Yes
PASSWORD_ECHO_MODE = QLineEdit.EchoMode.Password
TABLE_SELECT_ROWS = QAbstractItemView.SelectionBehavior.SelectRows
TABLE_SINGLE_SELECTION = QAbstractItemView.SelectionMode.SingleSelection
TABLE_NO_EDIT = QAbstractItemView.EditTrigger.NoEditTriggers


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$"
)


class MemberDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ho TEXT NOT NULL,
                    ten TEXT NOT NULL,
                    so_dien_thoai TEXT NOT NULL UNIQUE,
                    mat_khau TEXT NOT NULL,
                    ngay_sinh TEXT,
                    gioi_tinh TEXT NOT NULL
                )
                """
            )

    def add_member(self, data: dict):
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO members (ho, ten, so_dien_thoai, mat_khau, ngay_sinh, gioi_tinh)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data["ho"],
                    data["ten"],
                    data["so_dien_thoai"],
                    data["mat_khau"],
                    data["ngay_sinh"],
                    data["gioi_tinh"],
                ),
            )

    def get_members(self):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT id, ho, ten, so_dien_thoai, ngay_sinh, gioi_tinh
                FROM members
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()

    def get_member(self, member_id: int):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT id, ho, ten, so_dien_thoai, mat_khau, ngay_sinh, gioi_tinh
                FROM members
                WHERE id = ?
                """,
                (member_id,),
            )
            return cursor.fetchone()

    def update_member(self, member_id: int, data: dict):
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE members
                SET ho = ?, ten = ?, so_dien_thoai = ?, mat_khau = ?, ngay_sinh = ?, gioi_tinh = ?
                WHERE id = ?
                """,
                (
                    data["ho"],
                    data["ten"],
                    data["so_dien_thoai"],
                    data["mat_khau"],
                    data["ngay_sinh"],
                    data["gioi_tinh"],
                    member_id,
                ),
            )

    def delete_member(self, member_id: int):
        with self._connect() as connection:
            connection.execute("DELETE FROM members WHERE id = ?", (member_id,))


class MemberFormMixin:
    def setup_form(self):
        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.radioButton, 1)
        self.gender_group.addButton(self.radioButton_2, 2)
        self.lineEdit.setPlaceholderText("Họ")
        self.lineEdit_2.setPlaceholderText("Tên")
        self.lineEdit_3.setPlaceholderText("Số điện thoại")
        self.lineEdit_4.setPlaceholderText("Mật khẩu")
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_4.setEchoMode(PASSWORD_ECHO_MODE)
        self.populate_date_boxes()

    def populate_date_boxes(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()

        self.comboBox.addItem("Ngày", "")
        for day in range(1, 32):
            self.comboBox.addItem(str(day), day)

        self.comboBox_2.addItem("Tháng", "")
        for month in range(1, 13):
            self.comboBox_2.addItem(str(month), month)

        self.comboBox_3.addItem("Năm", "")
        for year in range(2026, 1929, -1):
            self.comboBox_3.addItem(str(year), year)

    def selected_gender(self):
        if self.radioButton.isChecked():
            return "Nam"
        if self.radioButton_2.isChecked():
            return "Nữ"
        return ""

    def selected_birth_date(self):
        day = self.comboBox.currentData()
        month = self.comboBox_2.currentData()
        year = self.comboBox_3.currentData()
        if day and month and year:
            return f"{day:02d}/{month:02d}/{year}"
        return ""

    def get_form_data(self):
        return {
            "ho": self.lineEdit.text().strip(),
            "ten": self.lineEdit_2.text().strip(),
            "so_dien_thoai": self.lineEdit_3.text().strip(),
            "mat_khau": self.lineEdit_4.text().strip(),
            "ngay_sinh": self.selected_birth_date(),
            "gioi_tinh": self.selected_gender(),
        }

    def validate_form(self, require_terms: bool):
        data = self.get_form_data()
        missing_fields = []

        if not data["ho"]:
            missing_fields.append("Họ")
        if not data["ten"]:
            missing_fields.append("Tên")
        if not data["so_dien_thoai"]:
            missing_fields.append("Số điện thoại")
        if not data["mat_khau"]:
            missing_fields.append("Mật khẩu")
        if not data["gioi_tinh"]:
            missing_fields.append("Giới tính")
        if require_terms and not self.checkBox.isChecked():
            missing_fields.append('Xác nhận "Tôi đồng ý với các điều khoản trên"')

        if missing_fields:
            self.show_warning(
                "Thiếu thông tin bắt buộc",
                "Vui lòng nhập/chọn đầy đủ:\n- " + "\n- ".join(missing_fields),
            )
            return None

        if not PASSWORD_PATTERN.match(data["mat_khau"]):
            self.show_warning(
                "Mật khẩu chưa đủ mạnh",
                (
                    "Mật khẩu phải có ít nhất 8 ký tự, gồm tối thiểu 1 chữ thường, "
                    "1 chữ hoa, 1 chữ số và 1 ký tự đặc biệt."
                ),
            )
            return None

        return data

    def set_form_data(self, member):
        self.lineEdit.setText(member["ho"])
        self.lineEdit_2.setText(member["ten"])
        self.lineEdit_3.setText(member["so_dien_thoai"])
        self.lineEdit_4.setText(member["mat_khau"])

        if member["gioi_tinh"] == "Nam":
            self.radioButton.setChecked(True)
        elif member["gioi_tinh"] == "Nữ":
            self.radioButton_2.setChecked(True)

        if member["ngay_sinh"]:
            day, month, year = member["ngay_sinh"].split("/")
            self.comboBox.setCurrentText(str(int(day)))
            self.comboBox_2.setCurrentText(str(int(month)))
            self.comboBox_3.setCurrentText(year)

    def clear_form(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.radioButton.setAutoExclusive(False)
        self.radioButton_2.setAutoExclusive(False)
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(True)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)

    def show_warning(self, title: str, message: str):
        QMessageBox.warning(self, title, message)


class RegistrationWindow(QMainWindow, MemberFormMixin):
    def __init__(self, database: MemberDatabase):
        super().__init__()
        uic.loadUi(str(BASE_DIR / "dangky.ui"), self)
        self.database = database
        self.list_window = None
        self.setup_form()
        self.setWindowTitle("Đăng ký thành viên")
        self.pushButton.clicked.connect(self.register_member)

    def register_member(self):
        data = self.validate_form(require_terms=True)
        if not data:
            return

        try:
            self.database.add_member(data)
        except sqlite3.IntegrityError:
            self.show_warning(
                "Không thể đăng ký",
                "Số điện thoại này đã tồn tại trong hệ thống.",
            )
            return

        QMessageBox.information(self, "Thành công", "Đăng ký thành công.")
        self.open_list_window()
        self.clear_form()

    def open_list_window(self):
        self.list_window = MemberListWindow(self.database, parent_registration=self)
        self.list_window.show()
        self.hide()


class MemberListWindow(QMainWindow):
    def __init__(self, database: MemberDatabase, parent_registration=None):
        super().__init__()
        uic.loadUi(str(BASE_DIR / "danhsach.ui"), self)
        self.database = database
        self.parent_registration = parent_registration
        self.edit_window = None
        self.setWindowTitle("Danh sách thành viên")
        self.configure_table()
        self.pushButton.clicked.connect(self.delete_selected_member)
        self.pushButton_2.clicked.connect(self.edit_selected_member)
        self.load_members()

    def configure_table(self):
        headers = ["Mã", "Họ", "Tên", "Số điện thoại", "Ngày sinh", "Giới tính"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setSelectionBehavior(TABLE_SELECT_ROWS)
        self.tableWidget.setSelectionMode(TABLE_SINGLE_SELECTION)
        self.tableWidget.setEditTriggers(TABLE_NO_EDIT)
        self.tableWidget.horizontalHeader().setSectionResizeMode(HEADER_STRETCH)

    def load_members(self):
        members = self.database.get_members()
        self.tableWidget.setRowCount(len(members))

        for row_index, member in enumerate(members):
            values = [
                member["id"],
                member["ho"],
                member["ten"],
                member["so_dien_thoai"],
                member["ngay_sinh"],
                member["gioi_tinh"],
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(int(ALIGN_CENTER))
                self.tableWidget.setItem(row_index, column_index, item)

    def selected_member_id(self):
        selected_ranges = self.tableWidget.selectedItems()
        if not selected_ranges:
            QMessageBox.warning(self, "Chưa chọn dòng", "Vui lòng chọn một thành viên.")
            return None

        row = selected_ranges[0].row()
        member_id_item = self.tableWidget.item(row, 0)
        return int(member_id_item.text())

    def delete_selected_member(self):
        member_id = self.selected_member_id()
        if member_id is None:
            return

        confirm = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa thành viên đã chọn không?",
        )
        if confirm != MESSAGEBOX_YES:
            return

        self.database.delete_member(member_id)
        self.load_members()
        QMessageBox.information(self, "Thành công", "Đã xóa thành viên.")

    def edit_selected_member(self):
        member_id = self.selected_member_id()
        if member_id is None:
            return

        self.edit_window = EditMemberWindow(self.database, member_id, self)
        self.edit_window.show()

    def refresh_after_edit(self):
        self.load_members()

    def closeEvent(self, event):
        if self.parent_registration is not None:
            self.parent_registration.show()
        super().closeEvent(event)


class EditMemberWindow(QMainWindow, MemberFormMixin):
    def __init__(self, database: MemberDatabase, member_id: int, list_window: MemberListWindow):
        super().__init__()
        uic.loadUi(str(BASE_DIR / "sua.ui"), self)
        self.database = database
        self.member_id = member_id
        self.list_window = list_window
        self.setWindowTitle("Sửa thông tin thành viên")
        self.setup_form()
        self.load_member_data()
        self.pushButton.clicked.connect(self.save_member)

    def load_member_data(self):
        member = self.database.get_member(self.member_id)
        if member is None:
            QMessageBox.warning(self, "Không tìm thấy", "Thành viên không còn tồn tại.")
            self.close()
            return
        self.set_form_data(member)

    def save_member(self):
        data = self.validate_form(require_terms=False)
        if not data:
            return

        try:
            self.database.update_member(self.member_id, data)
        except sqlite3.IntegrityError:
            self.show_warning(
                "Không thể lưu",
                "Số điện thoại này đã tồn tại trong hệ thống.",
            )
            return

        self.list_window.refresh_after_edit()
        QMessageBox.information(self, "Thành công", "Cập nhật thông tin thành viên thành công.")
        self.close()


def main():
    app = QApplication(sys.argv)
    database = MemberDatabase(DB_PATH)
    window = RegistrationWindow(database)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
