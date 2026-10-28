from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem
)
from PySide6.QtCore import Qt

import pandas as pd


class Dashboard(QWidget):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QVBoxLayout()

        # =========================
        # TITLE
        # =========================
        title = QLabel("Barcode Printing System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        layout.addWidget(title)

        # =========================
        # BUTTONS
        # =========================
        btn_print = QPushButton("Print Label")
        btn_batch = QPushButton("Batch Print")
        btn_designer = QPushButton("Label Designer")
        btn_printer = QPushButton("Printer Settings")

        # ✅ NEW
        btn_import_excel = QPushButton("Import Excel")

        btn_next = QPushButton("Next → Map to Label")

        buttons = [
            btn_print,
            btn_batch,
            btn_designer,
            btn_printer,
            btn_import_excel,
            btn_next
        ]

        for btn in buttons:
            btn.setFixedHeight(50)
            btn.setStyleSheet("font-size: 16px;")
            layout.addWidget(btn)

        # =========================
        # TABLE
        # =========================
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        # =========================
        # CONNECTIONS
        # =========================
        btn_designer.clicked.connect(
            self.main_window.show_label_designer
        )

        btn_next.clicked.connect(self.goto_mapping)

        # ✅ EXCEL IMPORT
        btn_import_excel.clicked.connect(
            self.import_excel
        )

    # =========================
    # IMPORT EXCEL
    # =========================
    def import_excel(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            # clear table
            self.table.setRowCount(0)

            # set columns
            self.table.setColumnCount(len(df.columns))
            self.table.setHorizontalHeaderLabels(
                df.columns.tolist()
            )

            # add rows
            for row_data in df.values.tolist():

                row = self.table.rowCount()
                self.table.insertRow(row)

                for col, value in enumerate(row_data):

                    item = QTableWidgetItem(str(value))

                    self.table.setItem(
                        row,
                        col,
                        item
                    )

            print("Excel Imported Successfully ✅")

        except Exception as e:
            print("Excel Import Error ❌")
            print(e)

    # =========================
    # GOTO MAPPING
    # =========================
    def goto_mapping(self):

        row = self.table.currentRow()

        if row < 0:
            print("Select a row first ❌")
            return

        selected_data = {}

        # get headers
        for col in range(self.table.columnCount()):

            header = self.table.horizontalHeaderItem(col)

            if header:
                key = header.text()

                item = self.table.item(row, col)

                selected_data[key] = (
                    item.text() if item else ""
                )

        # send to main window
        self.main_window.selected_data = selected_data

        print("Selected Data:")
        print(selected_data)

        # open mapping
        self.main_window.goto_mapping()