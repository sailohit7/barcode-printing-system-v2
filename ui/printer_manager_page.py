from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QMessageBox,
    QHeaderView
)

from PySide6.QtCore import Qt

from printer.printer_manager import PrinterManager


class PrinterManagerPage(QWidget):

    def __init__(self):
        super().__init__()

        self.manager = PrinterManager()

        self.build_ui()

        self.load_printers()

    # --------------------------------------------------

    def build_ui(self):

        main = QVBoxLayout(self)

        title = QLabel("🖨 Printer Manager")
        title.setStyleSheet("""
            QLabel{
                font-size:24px;
                font-weight:bold;
                padding:10px;
            }
        """)

        main.addWidget(title)

        # ============================
        # Printer List
        # ============================

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Printer",
            "Driver",
            "Port",
            "Status",
            "Default"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.itemSelectionChanged.connect(
            self.show_details
        )

        main.addWidget(self.table)

        # ============================

        self.details = QTextEdit()

        self.details.setReadOnly(True)

        main.addWidget(self.details)

        # ============================

        buttons = QHBoxLayout()

        self.refresh_btn = QPushButton("🔄 Refresh")

        self.default_btn = QPushButton("⭐ Set Default")

        self.test_btn = QPushButton("🧾 Test Print")

        buttons.addWidget(self.refresh_btn)

        buttons.addWidget(self.default_btn)

        buttons.addWidget(self.test_btn)

        main.addLayout(buttons)

        self.refresh_btn.clicked.connect(
            self.load_printers
        )

        self.default_btn.clicked.connect(
            self.set_default
        )

        self.test_btn.clicked.connect(
            self.test_print
        )

    # --------------------------------------------------

    def load_printers(self):

        printers = self.manager.get_printers()

        self.printers = printers

        self.table.setRowCount(len(printers))

        for row, p in enumerate(printers):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(p["name"])
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(p["driver"])
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(p["port"])
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(p["status"])
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    "Yes" if p["default"] else ""
                )
            )

    # --------------------------------------------------

    def current_printer(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return self.printers[row]

    # --------------------------------------------------

    def show_details(self):

        printer = self.current_printer()

        if not printer:
            return

        txt = f"""

Printer Name

{printer["name"]}


Driver

{printer["driver"]}


Port

{printer["port"]}


Status

{printer["status"]}


Default

{printer["default"]}

"""

        self.details.setText(txt)

    # --------------------------------------------------

    def set_default(self):

        printer = self.current_printer()

        if not printer:
            return

        ok = self.manager.set_default(
            printer["name"]
        )

        if ok:

            QMessageBox.information(
                self,
                "Success",
                "Default printer changed."
            )

            self.load_printers()

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Unable to set default printer."
            )

    # --------------------------------------------------

    def test_print(self):

        printer = self.current_printer()

        if not printer:
            return

        ok = self.manager.print_test_page(
            printer["name"]
        )

        if ok:

            QMessageBox.information(
                self,
                "Success",
                "Test print sent."
            )

        else:

            QMessageBox.warning(
                self,
                "Failed",
                "Unable to print."
            )