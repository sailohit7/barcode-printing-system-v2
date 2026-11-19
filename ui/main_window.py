from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QToolBar,
    QComboBox, QInputDialog, QLineEdit,
    QTableWidget, QTableWidgetItem,
    QFileDialog, QTextEdit, QHeaderView, QFrame, QGraphicsOpacityEffect, QMessageBox,
    QGridLayout, QAbstractItemView, QSplitter, QScrollArea, QSlider, QCheckBox,
    QSpinBox, QDoubleSpinBox, QSizePolicy, QGraphicsView
)

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRectF
from PySide6.QtGui import QAction, QFont, QBrush, QColor, QPainter
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

import pandas as pd
import os
import json


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barcode Printing System")
        self.resize(1400, 850)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # =======================
        # SIDEBAR
        # =======================
        sidebar_panel = QFrame()
        sidebar_panel.setObjectName("Sidebar")
        sidebar_panel.setFixedWidth(225)
        sidebar = QVBoxLayout(sidebar_panel)
        sidebar.setContentsMargins(14, 20, 14, 16)
        sidebar.setSpacing(8)

        brand = QLabel("BARCODE\nSTUDIO")
        brand.setObjectName("BrandTitle")
        brand.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        sidebar.addWidget(brand)

        tagline = QLabel("LABEL OPERATIONS")
        tagline.setObjectName("BrandTagline")
        sidebar.addWidget(tagline)
        sidebar.addSpacing(24)

        self.btn_dashboard = QPushButton("▦   Dashboard")
        self.btn_designer = QPushButton("✎   Label Designer")
        self.btn_printer = QPushButton("▤   Printer Manager")
        self.btn_connection = QPushButton("⌁   Printer Connection")
        self.btn_history = QPushButton("◷   SQL History")
        self.btn_database = QPushButton("⚙   Database Settings")

        self.nav_buttons = [
            self.btn_dashboard, self.btn_designer, self.btn_printer,
            self.btn_connection, self.btn_history, self.btn_database
        ]
        for button in self.nav_buttons:
            button.setObjectName("NavButton")
            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumHeight(44)
            sidebar.addWidget(button)

        sidebar.addStretch()

        sidebar_footer = QLabel("BARCODE PRINTING SYSTEM\nDesktop Edition")
        sidebar_footer.setObjectName("SidebarFooter")
        sidebar.addWidget(sidebar_footer)
        # =======================
        # STACK
        # =======================
        self.stack = QStackedWidget()
        self.stack.setObjectName("PageStack")

        self.dashboard = self.build_dashboard()
        self.designer = self.build_designer()
        self.mapping_screen = self.build_mapping_screen()
        self.print_screen = self.build_print_screen()
        self.printer_screen = self.build_printer_screen()
        self.connection_screen = self.build_connection_screen()

        # NEW
        self.history_screen = self.build_history_screen()
        self.database_screen = self.build_database_screen()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.designer)
        self.stack.addWidget(self.mapping_screen)
        self.stack.addWidget(self.print_screen)
        self.stack.addWidget(self.printer_screen)
        self.stack.addWidget(self.connection_screen)
        self.stack.addWidget(self.history_screen)
        self.stack.addWidget(self.database_screen)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(sidebar_panel)

        content_panel = QWidget()
        content_layout = QVBoxLayout(content_panel)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        self.page_heading = QLabel("Dashboard")
        self.page_heading.setObjectName("PageHeading")
        self.page_subheading = QLabel("Manage products, labels, and print operations.")
        self.page_subheading.setObjectName("PageSubheading")
        content_layout.addWidget(self.page_heading)
        content_layout.addWidget(self.page_subheading)
        content_layout.addWidget(self.stack, 1)
        main_layout.addWidget(content_panel, 1)

        self._page_animation = None
        self.init_toolbar()

        # =======================
        # NAVIGATION
        # =======================
        self.btn_dashboard.clicked.connect(lambda: self.show_page(self.dashboard, self.btn_dashboard, "Dashboard", "Manage products, labels, and print operations."))
        self.btn_designer.clicked.connect(lambda: self.show_page(self.designer, self.btn_designer, "Label Designer", "Build and arrange your label elements."))
        self.btn_printer.clicked.connect(lambda: self.show_page(self.printer_screen, self.btn_printer, "Printer Manager", "Select an installed printer and refresh the device list."))
        self.btn_connection.clicked.connect(lambda: self.show_page(self.connection_screen, self.btn_connection, "Printer Connection", "Inspect printer status, ports, drivers, and test printing."))
        self.btn_history.clicked.connect(self.open_history_page)
        self.btn_database.clicked.connect(lambda: self.show_page(self.database_screen, self.btn_database, "Database Settings", "Configure SQL Server for this computer."))
        self.show_page(self.dashboard, self.btn_dashboard, "Dashboard", "Manage products, labels, and print operations.", animate=False)

        # =======================
        # STYLE
        # =======================
        self.setStyleSheet("""
            QWidget {
                background-color: #10141d;
                color: #e8edf7;
                font-size: 13px;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QFrame#Sidebar {
                background-color: #0b0f17;
                border-right: 1px solid #242c3b;
            }
            QFrame#MetricCard, QFrame#Panel {
                background-color: #151c28;
                border: 1px solid #29354a;
                border-radius: 12px;
            }
            QLabel#MetricTitle {
                color: #7f91ad;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1px;
                background: transparent;
            }
            QLabel#MetricValue {
                color: #f5f8ff;
                font-size: 25px;
                font-weight: 800;
                background: transparent;
            }
            QLabel#MetricHint {
                color: #8290a7;
                font-size: 11px;
                background: transparent;
            }
            QLabel#BrandTitle {
                color: #f4f7ff;
                font-size: 21px;
                font-weight: 800;
                letter-spacing: 1px;
            }
            QLabel#BrandTagline {
                color: #73819a;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }
            QLabel#SidebarFooter {
                color: #65718a;
                font-size: 10px;
                padding: 10px 2px;
                border-top: 1px solid #222a38;
            }
            QLabel#PageHeading {
                color: #f6f8fc;
                font-size: 26px;
                font-weight: 750;
                padding: 0;
            }
            QLabel#PageSubheading {
                color: #8995aa;
                font-size: 12px;
                padding-bottom: 6px;
            }
            QPushButton {
                background-color: #202838;
                color: #e8edf7;
                border: 1px solid #2b3548;
                border-radius: 9px;
                padding: 10px 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2b3850;
                border-color: #4f7cff;
            }
            QPushButton#PrimaryButton {
                background-color: #315fd1;
                border: 1px solid #4778ec;
                color: white;
            }
            QPushButton#PrimaryButton:hover {
                background-color: #3b70ee;
            }
            QPushButton:pressed { background-color: #172238; }
            QPushButton#NavButton {
                background-color: transparent;
                color: #9ca9bf;
                text-align: left;
                border: 1px solid transparent;
                padding: 12px 13px;
                font-weight: 600;
            }
            QPushButton#NavButton:hover {
                background-color: #171f2d;
                color: #f5f8ff;
                border-color: #263247;
            }
            QPushButton#NavButton[active="true"] {
                background-color: #1d2e4b;
                color: #8db7ff;
                border: 1px solid #31558a;
            }
            QLineEdit, QComboBox, QTableWidget, QTextEdit {
                background-color: #151c28;
                color: #e8edf7;
                border: 1px solid #2a3548;
                border-radius: 7px;
                padding: 8px;
                selection-background-color: #31558a;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #5d91ff;
            }
            QTableWidget {
                gridline-color: #273143;
                alternate-background-color: #182130;
                selection-background-color: #263e64;
                border-radius: 9px;
            }
            QHeaderView::section {
                background-color: #202a3a;
                color: #b8c5d9;
                padding: 9px;
                border: none;
                border-bottom: 1px solid #334158;
                font-weight: 700;
            }
            QComboBox QAbstractItemView {
                background-color: #151c28;
                selection-background-color: #263e64;
            }
            QToolBar {
                background-color: #0b0f17;
                border: none;
                border-bottom: 1px solid #242c3b;
                spacing: 8px;
                padding: 6px;
            }
        """)

    # =========================================================
    # DASHBOARD
    # =========================================================
    def build_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        self.fields_config = ["name", "sku", "price", "qty"]
        self.table = QTableWidget(0, len(self.fields_config))
        self.table.setObjectName("DataTable")
        self.table.setHorizontalHeaderLabels([field.upper() for field in self.fields_config])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        # Dashboard metric cards
        metrics = QHBoxLayout()
        metrics.setSpacing(12)
        self.metric_products = self._make_metric_card("PRODUCT ROWS", "0", "Products loaded or entered")
        self.metric_fields = self._make_metric_card("DATA FIELDS", "4", "Columns available for mapping")
        self.metric_printers = self._make_metric_card("INSTALLED PRINTERS", "…", "Windows printer devices")
        self.metric_canvas = self._make_metric_card("LABEL ELEMENTS", "0", "Elements on the design canvas")
        for card in (self.metric_products, self.metric_fields, self.metric_printers, self.metric_canvas):
            metrics.addWidget(card["frame"], 1)
        layout.addLayout(metrics)

        controls = QHBoxLayout()
        controls.setSpacing(8)
        btn_add_field = QPushButton("+  Add Field")
        btn_remove_field = QPushButton("−  Remove Field")
        btn_import_excel = QPushButton("⇧  Import Excel")
        controls.addWidget(btn_add_field)
        controls.addWidget(btn_remove_field)
        controls.addWidget(btn_import_excel)
        controls.addStretch()
        layout.addLayout(controls)

        self.form_layout = QHBoxLayout()
        self.form_layout.setSpacing(10)
        self.inputs = {}
        self.build_form()
        form_frame = QFrame()
        form_frame.setObjectName("Panel")
        form_frame.setLayout(self.form_layout)
        layout.addWidget(form_frame)

        btn_add = QPushButton("＋  Add Entry")
        btn_add.setObjectName("PrimaryButton")
        btn_save = QPushButton("Save Product to SQL History")
        btn_test_sql = QPushButton("Test SQL Connection")
        btn_next = QPushButton("Generate Label  →")
        actions = QHBoxLayout()
        actions.addWidget(btn_add, 2)
        actions.addWidget(btn_save, 1)
        actions.addWidget(btn_test_sql, 1)
        actions.addWidget(btn_next, 1)
        layout.addLayout(actions)

        self.table.setMinimumHeight(220)
        layout.addWidget(self.table, 1)

        btn_add_field.clicked.connect(self.add_field)
        btn_remove_field.clicked.connect(self.remove_field)
        btn_add.clicked.connect(self.add_entry)
        btn_save.clicked.connect(self.save_history)
        btn_test_sql.clicked.connect(self.test_sql_connection)
        btn_next.clicked.connect(self.goto_mapping)
        btn_import_excel.clicked.connect(self.import_excel)

        self._refresh_dashboard_metrics()
        return page

    def _make_metric_card(self, label, value, hint):
        frame = QFrame()
        frame.setObjectName("MetricCard")
        box = QVBoxLayout(frame)
        box.setContentsMargins(16, 13, 16, 13)
        box.setSpacing(5)
        title = QLabel(label)
        title.setObjectName("MetricTitle")
        value_label = QLabel(value)
        value_label.setObjectName("MetricValue")
        hint_label = QLabel(hint)
        hint_label.setObjectName("MetricHint")
        hint_label.setWordWrap(True)
        box.addWidget(title)
        box.addWidget(value_label)
        box.addWidget(hint_label)
        return {"frame": frame, "value": value_label}

    def _refresh_dashboard_metrics(self):
        if hasattr(self, "metric_products"):
            self.metric_products["value"].setText(str(self.table.rowCount()))
            self.metric_fields["value"].setText(str(len(self.fields_config)))
        if hasattr(self, "metric_canvas") and hasattr(self, "canvas"):
            try:
                count = max(0, len(self.canvas.scene.items()) - 1)
            except Exception:
                count = 0
            self.metric_canvas["value"].setText(str(count))
        if hasattr(self, "metric_printers"):
            try:
                count = len(self._printer_manager().get_printers())
                self.metric_printers["value"].setText(str(count))
            except Exception:
                self.metric_printers["value"].setText("—")

        # =========================================================
        # BUILD FORM
        # =========================================================
    def build_form(self):

        while self.form_layout.count():
            item = self.form_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        self.inputs.clear()

        for field in self.fields_config:

            box = QVBoxLayout()

            label = QLabel(field.upper())

            input_box = QLineEdit()

            self.inputs[field] = input_box

            box.addWidget(label)
            box.addWidget(input_box)

            self.form_layout.addLayout(box)

        self.table.setColumnCount(len(self.fields_config))
        self.table.setHorizontalHeaderLabels([str(field).upper() for field in self.fields_config])
        if hasattr(self, 'metric_fields'):
            self.metric_fields['value'].setText(str(len(self.fields_config)))

    # =========================================================
    # IMPORT EXCEL
    # =========================================================
    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import product data", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv)"
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            if df.empty or len(df.columns) == 0:
                QMessageBox.information(self, "No data", "The selected file does not contain any rows or columns.")
                return
            self.table.setRowCount(0)
            self.fields_config = [str(column).strip() or f"field_{i+1}" for i, column in enumerate(df.columns)]
            self.build_form()
            self.table.setColumnCount(len(self.fields_config))
            self.table.setHorizontalHeaderLabels([field.upper() for field in self.fields_config])
            for row_data in df.fillna("").values.tolist():
                row = self.table.rowCount()
                self.table.insertRow(row)
                for col, value in enumerate(row_data):
                    self.table.setItem(row, col, QTableWidgetItem(str(value)))
            self._refresh_dashboard_metrics()
            QMessageBox.information(self, "Import complete", f"Imported {len(df)} row(s) from:\n{os.path.basename(file_path)}")
        except Exception as exc:
            QMessageBox.critical(self, "Import failed", f"Could not import the selected file.\n\n{exc}")

        # =========================================================
        # FIELD CONTROLS
        # =========================================================
    def add_field(self):

        name, ok = QInputDialog.getText(
            self,
            "Add Field",
            "Field name:"
        )

        name = name.strip()
        if ok and name:
            if any(str(field).casefold() == name.casefold() for field in self.fields_config):
                QMessageBox.information(self, "Field exists", "A field with that name already exists.")
                return
            self.fields_config.append(name)
            self.build_form()
            self._refresh_dashboard_metrics()

    def remove_field(self):

        if len(self.fields_config) > 1:
            self.fields_config.pop()
            self.build_form()
            self._refresh_dashboard_metrics()
        else:
            QMessageBox.information(self, "Keep one field", "At least one data field is required.")

    # =========================================================
    # ENTRY
    # =========================================================
    def add_entry(self):

        row = self.table.rowCount()
        self.table.insertRow(row)

        for col, field in enumerate(self.fields_config):

            value = self.inputs[field].text()

            self.table.setItem(
                row,
                col,
                QTableWidgetItem(value)
            )

        for inp in self.inputs.values():
            inp.clear()
        self._refresh_dashboard_metrics()

    # =========================================================
    # SAVE HISTORY
    # =========================================================
    def save_history(self):
        rows = sorted({index.row() for index in self.table.selectionModel().selectedRows()})
        if not rows and self.table.currentRow() >= 0:
            rows = [self.table.currentRow()]
        if not rows:
            QMessageBox.information(self, "Select products", "Select one or more product rows before saving history.")
            return
        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager()
            for row in rows:
                data = {}
                for col, field in enumerate(self.fields_config):
                    item = self.table.item(row, col)
                    data[str(field).strip().lower()] = item.text() if item else ""
                db.save_print_history(data)
            QMessageBox.information(self, "History saved", f"Saved {len(rows)} selected product record(s) to SQL Server.")
            if hasattr(self, "history_table"):
                self.load_sql_history()
        except Exception as exc:
            QMessageBox.warning(self, "SQL Server unavailable", f"Could not save history.\n\n{exc}")
        finally:
            if db:
                try: db.close()
                except Exception: pass

    def test_sql_connection(self):
        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager()
            result = db.test()
            QMessageBox.information(
                self, "SQL Server Connected",
                f"Connection successful. SQL Server returned: {result[0] if result else 'OK'}"
            )
        except Exception as exc:
            QMessageBox.critical(
                self, "SQL Server Connection Failed",
                "Could not connect to SQL Server. Check database/sql_manager.py for the server, database, ODBC driver, and authentication settings.\\n\\n" + str(exc)
            )
        finally:
            if db:
                try:
                    db.close()
                except Exception:
                    pass

    def build_mapping_screen(self):
        page = QWidget()
        self.mapping_layout = QVBoxLayout(page)
        self.mapping_layout.setSpacing(12)

        title = QLabel("Field Mapping & Barcode Customization")
        title.setObjectName("PageHeading")
        self.mapping_help = QLabel(
            "Choose how each product field appears. Set barcode format, height, scale and readable value, "
            "then preview and customize the label before printing."
        )
        self.mapping_help.setWordWrap(True)
        self.mapping_help.setObjectName("MetricHint")

        options = QHBoxLayout()
        options.addWidget(QLabel("Barcode format"))
        self.mapping_barcode_type = QComboBox()
        self.mapping_barcode_type.addItems(["CODE128", "CODE39", "EAN13"])
        options.addWidget(self.mapping_barcode_type)

        options.addWidget(QLabel("Height"))
        self.mapping_barcode_height = QSpinBox()
        self.mapping_barcode_height.setRange(30, 180)
        self.mapping_barcode_height.setValue(70)
        self.mapping_barcode_height.setSuffix(" px")
        options.addWidget(self.mapping_barcode_height)

        options.addWidget(QLabel("Scale"))
        self.mapping_barcode_scale = QDoubleSpinBox()
        self.mapping_barcode_scale.setRange(0.25, 3.0)
        self.mapping_barcode_scale.setSingleStep(0.25)
        self.mapping_barcode_scale.setValue(1.0)
        self.mapping_barcode_scale.setSuffix("×")
        options.addWidget(self.mapping_barcode_scale)

        self.mapping_barcode_text = QCheckBox("Show barcode value")
        self.mapping_barcode_text.setChecked(True)
        options.addWidget(self.mapping_barcode_text)
        options.addStretch()

        self.mapping_layout.addWidget(title)
        self.mapping_layout.addWidget(self.mapping_help)
        self.mapping_layout.addLayout(options)
        self.btn_mapping_preview = QPushButton("Generate Preview → Customize → Print")
        self.btn_mapping_preview.setObjectName("PrimaryButton")
        self.btn_mapping_preview.clicked.connect(self.generate_preview)
        self.mapping_layout.addWidget(self.btn_mapping_preview)
        return page

    # =========================================================
    # GOTO MAPPING
    # =========================================================
    def goto_mapping(self):
        rows = sorted({index.row() for index in self.table.selectionModel().selectedRows()})
        if not rows and self.table.currentRow() >= 0:
            rows = [self.table.currentRow()]
        if not rows:
            QMessageBox.information(self, "Select products", "Select one or more product rows from the Dashboard.")
            return
        self.selected_product_rows = []
        for row in rows:
            record = {}
            for col, field in enumerate(self.fields_config):
                item = self.table.item(row, col)
                record[field] = item.text() if item else ""
            self.selected_product_rows.append(record)
        self.selected_data = self.selected_product_rows[0]
        self.load_mapping_ui()
        self.stack.setCurrentWidget(self.mapping_screen)

    # =========================================================
    # LOAD MAPPING
    # =========================================================
    def load_mapping_ui(self):
        # Keep the title, help, barcode options and preview button; rebuild only field rows.
        while self.mapping_layout.count() > 4:
            item = self.mapping_layout.takeAt(3)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        self.mapping_widgets = []
        for field in self.fields_config:
            row = QHBoxLayout()
            row.addWidget(QLabel(str(field).upper()))
            dropdown = QComboBox()
            dropdown.addItems(["None", "Text", "Barcode", "QR"])
            normalized = str(field).strip().casefold()
            if normalized in ("sku", "barcode", "barcode_value", "product_code", "code", "ean", "upc"):
                dropdown.setCurrentText("Barcode")
            elif normalized in ("name", "product", "productname", "product_name", "title", "price", "qty", "quantity"):
                dropdown.setCurrentText("Text")
            row.addWidget(dropdown)
            self.mapping_layout.insertLayout(self.mapping_layout.count() - 1, row)
            self.mapping_widgets.append((field, dropdown))

    # =========================================================
    # GENERATE PREVIEW
    # =========================================================
    def generate_preview(self):
        if not getattr(self, "selected_data", None):
            QMessageBox.information(self, "Select a product", "Choose a product row from Dashboard first.")
            return
        barcode_format = self.mapping_barcode_type.currentText()
        if barcode_format == "EAN13":
            barcode_value = next(
                (str(self.selected_data.get(field, "")).strip()
                 for field, dropdown in self.mapping_widgets
                 if dropdown.currentText() == "Barcode" and self.selected_data.get(field)),
                ""
            )
            if not barcode_value:
                barcode_value = next(
                    (str(v).strip() for k, v in self.selected_data.items()
                     if str(k).strip().casefold() in ("sku", "barcode", "barcode_value", "product_code", "code", "ean", "upc") and v),
                    ""
                )
            if not barcode_value.isdigit() or len(barcode_value) not in (12, 13):
                QMessageBox.warning(
                    self, "EAN-13 needs numeric data",
                    "EAN-13 supports a 12-digit number (checksum added automatically) or a 13-digit number. "
                    "Your sample SKUs contain letters, so choose CODE128 or CODE39 instead."
                )
                return
        self.canvas.clear_canvas()
        self.canvas.label_rect.setZValue(-100)
        y = 16
        has_barcode = False
        for field, dropdown in self.mapping_widgets:
            value = str(self.selected_data.get(field, ""))
            choice = dropdown.currentText()
            if not value or choice == "None":
                continue
            if choice == "Text":
                item = self.canvas.add_text_direct(f"{field}: {value}")
                item.setPos(18, y)
                y += max(32, item.boundingRect().height() + 8)
            elif choice == "Barcode":
                item = self.canvas.add_barcode_direct(
                    value,
                    barcode_type=self.mapping_barcode_type.currentText(),
                    height=self.mapping_barcode_height.value(),
                    scale=self.mapping_barcode_scale.value(),
                    show_text=self.mapping_barcode_text.isChecked(),
                )
                item.setPos(18, y)
                has_barcode = True
                y += self.mapping_barcode_height.value() * self.mapping_barcode_scale.value() + 25
            elif choice == "QR":
                item = self.canvas.add_qr_direct(value)
                item.setPos(18, y)
                y += 100
        if not has_barcode:
            sku_key = next((k for k in self.selected_data if str(k).strip().casefold() in
                            ("sku", "barcode", "barcode_value", "product_code", "code", "ean", "upc")), None)
            if sku_key and self.selected_data.get(sku_key):
                item = self.canvas.add_barcode_direct(
                    str(self.selected_data[sku_key]),
                    barcode_type=self.mapping_barcode_type.currentText(),
                    height=self.mapping_barcode_height.value(),
                    scale=self.mapping_barcode_scale.value(),
                    show_text=self.mapping_barcode_text.isChecked(),
                )
                item.setPos(18, y)
                has_barcode = True
        if not has_barcode:
            QMessageBox.warning(self, "No barcode field mapped",
                "No SKU/code field is available. Map the SKU field to Barcode to generate a barcode.")
        self._refresh_dashboard_metrics()
        self.stack.setCurrentWidget(self.print_screen)
        self.copies_input.setText("1")
        self._update_print_summary()

    def _update_print_summary(self):
        if not hasattr(self, "print_summary"):
            return
        data = getattr(self, "selected_data", {}) or {}
        name = next((v for k, v in data.items() if str(k).strip().casefold() in ("name", "product", "product_name", "productname")), "")
        sku = next((v for k, v in data.items() if str(k).strip().casefold() in ("sku", "barcode", "barcode_value", "product_code", "code")), "")
        count = len(getattr(self, "selected_product_rows", []) or [data])
        suffix = f"    |    Batch: {count} product(s)" if count > 1 else ""
        self.print_summary.setText(f"Product: {name or '—'}    |    SKU / Barcode: {sku or '—'}{suffix}")

    # =========================================================
    # PRINT SCREEN
    # =========================================================
    def build_print_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(14)
        title = QLabel("Print Labels")
        title.setObjectName("PageHeading")
        subtitle = QLabel("Review the product, choose a printer, then print and save the print record.")
        subtitle.setObjectName("PageSubheading")
        self.print_summary = QLabel("Product: —    |    SKU / Barcode: —")
        self.print_summary.setWordWrap(True)
        self.print_summary.setObjectName("MetricHint")
        self.copies_input = QLineEdit()
        self.copies_input.setPlaceholderText("Number of copies (default 1)")
        self.copies_input.setText("1")
        self.print_printer_combo = QComboBox()
        self.print_printer_combo.setMinimumHeight(42)
        self.print_status_label = QLabel("Printing sends the current label canvas to the selected printer.")
        self.print_status_label.setWordWrap(True)
        self.print_status_label.setObjectName("MetricHint")
        btn_print = QPushButton("Print Label and Save to SQL")
        btn_print.setObjectName("PrimaryButton")
        btn_back = QPushButton("← Back to Mapping")
        btn_customize = QPushButton("✎ Customize Label")
        btn_refresh = QPushButton("↻ Refresh Printers")
        for widget in (title, subtitle, self.print_summary, QLabel("Printer"), self.print_printer_combo,
                       QLabel("Copies"), self.copies_input, self.print_status_label):
            layout.addWidget(widget)
        buttons = QHBoxLayout()
        buttons.addWidget(btn_back)
        buttons.addWidget(btn_customize)
        buttons.addWidget(btn_refresh)
        buttons.addWidget(btn_print, 2)
        layout.addLayout(buttons)
        layout.addStretch(1)
        btn_print.clicked.connect(self.handle_print)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.mapping_screen))
        btn_customize.clicked.connect(
            lambda: self.show_page(self.designer, self.btn_designer, "Label Designer",
                                   "Customize the selected product label before printing.")
        )
        btn_refresh.clicked.connect(self.load_print_printers)
        self.load_print_printers()
        return page

    def load_print_printers(self):
        current = self.print_printer_combo.currentText() if hasattr(self, "print_printer_combo") else ""
        self.print_printer_combo.clear()
        try:
            from printer.printer_manager import PrinterManager
            printers = PrinterManager().get_printers()
            for printer in printers:
                if printer.get("name"):
                    self.print_printer_combo.addItem(printer["name"])
            default_name = next((p.get("name") for p in printers if p.get("default")), "")
            if default_name:
                self.print_printer_combo.setCurrentText(default_name)
            elif current:
                self.print_printer_combo.setCurrentText(current)
            if not printers:
                self.print_printer_combo.addItem("No printers found")
        except Exception as exc:
            self.print_printer_combo.addItem("Printer service unavailable")
            self.print_status_label.setText(f"Could not enumerate Windows printers: {exc}")

    def _build_canvas_for_product(self, product_data):
        """Render one product record into the label canvas using current field mappings."""
        self.canvas.clear_canvas()
        self.canvas.label_rect.setZValue(-100)
        y = 16
        has_barcode = False
        for field, dropdown in self.mapping_widgets:
            value = str(product_data.get(field, ""))
            choice = dropdown.currentText()
            if not value or choice == "None":
                continue
            if choice == "Text":
                item = self.canvas.add_text_direct(f"{field}: {value}")
                item.setPos(18, y)
                y += max(32, item.boundingRect().height() + 8)
            elif choice == "Barcode":
                item = self.canvas.add_barcode_direct(
                    value, barcode_type=self.mapping_barcode_type.currentText(),
                    height=self.mapping_barcode_height.value(),
                    scale=self.mapping_barcode_scale.value(),
                    show_text=self.mapping_barcode_text.isChecked())
                item.setPos(18, y)
                has_barcode = True
                y += self.mapping_barcode_height.value() * self.mapping_barcode_scale.value() + 25
            elif choice == "QR":
                item = self.canvas.add_qr_direct(value)
                item.setPos(18, y)
                y += 100
        if not has_barcode:
            sku_key = next((k for k in product_data if str(k).strip().casefold() in
                            ("sku", "barcode", "barcode_value", "product_code", "code", "ean", "upc")
                            and product_data.get(k)), None)
            if sku_key:
                item = self.canvas.add_barcode_direct(
                    str(product_data[sku_key]), barcode_type=self.mapping_barcode_type.currentText(),
                    height=self.mapping_barcode_height.value(),
                    scale=self.mapping_barcode_scale.value(),
                    show_text=self.mapping_barcode_text.isChecked())
                item.setPos(18, y)
                has_barcode = True
        if not has_barcode:
            raise ValueError("No barcode field is mapped and no SKU/code value is available.")

    def handle_print(self):
        raw_copies = self.copies_input.text().strip() or "1"
        try:
            copies = int(raw_copies)
            if copies < 1 or copies > 10000:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid copies", "Enter a whole number from 1 to 10000.")
            return
        product_records = getattr(self, "selected_product_rows", None) or ([self.selected_data] if getattr(self, "selected_data", None) else [])
        if not product_records:
            QMessageBox.information(self, "No products selected", "Return to Dashboard and select one or more products first.")
            return
        printer_name = self.print_printer_combo.currentText().strip()
        if not printer_name or printer_name in ("No printers found", "Printer service unavailable"):
            QMessageBox.warning(self, "No printer selected", "Install or select an available Windows printer first.")
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setPrinterName(printer_name)
            printer.setCopyCount(copies)
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Print Label")
            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                self.print_status_label.setText("Printing cancelled; no SQL print-history record was created.")
                return
            painter = QPainter()
            if not painter.begin(printer):
                raise RuntimeError("Could not start the printer painter. Check the printer driver and queue.")
            try:
                page_rect = QRectF(painter.viewport())
                for index, product_data in enumerate(product_records):
                    if index > 0 and not printer.newPage():
                        raise RuntimeError("The printer could not start the next label page.")
                    self._build_canvas_for_product(product_data)
                    source_rect = self.canvas.label_rect.rect()
                    self.canvas.scene.render(painter, page_rect, source_rect, Qt.AspectRatioMode.KeepAspectRatio)
            finally:
                painter.end()
        except Exception as exc:
            QMessageBox.critical(self, "Print failed",
                f"The label could not be sent to the printer. No SQL history record was saved.\n\n{exc}")
            return

        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager()
            for product_data in product_records:
                normalized = {str(k).strip().casefold(): v for k, v in product_data.items()}
                db.save_print({
                    "name": normalized.get("name", normalized.get("product", normalized.get("product_name", ""))),
                    "sku": normalized.get("sku", normalized.get("barcode", normalized.get("product_code", ""))),
                    "price": normalized.get("price", ""),
                    "qty": normalized.get("qty", normalized.get("quantity", "")),
                }, printer_name, copies)
            self.print_status_label.setText(f"Submitted {len(product_records)} label(s) to {printer_name}; {copies} copy/copies each. SQL history saved.")
            QMessageBox.information(self, "Batch print submitted",
                f"Sent {len(product_records)} selected product label(s) to {printer_name}, {copies} copy/copies each. SQL history was saved.")
            if hasattr(self, "history_table"):
                self.load_sql_history()
        except Exception as exc:
            self.print_status_label.setText("Print job submitted, but SQL history could not be saved.")
            QMessageBox.warning(self, "Printed; SQL save failed",
                "The print job was submitted, but the print-history record could not be saved. Check SQL settings and schema.\n\n" + str(exc))
        finally:
            if db:
                try: db.close()
                except Exception: pass

    def build_printer_screen(self):

        w = QWidget()

        layout = QVBoxLayout(w)

        title = QLabel("Printer Manager")
        title.setAlignment(Qt.AlignCenter)

        self.printer_list = QComboBox()

        self.printer_list.addItems([
            "Default Printer"
        ])

        btn_refresh = QPushButton("Refresh Printers")
        btn_refresh.clicked.connect(self.load_printer_list)

        layout.addWidget(title)
        layout.addWidget(self.printer_list)
        layout.addWidget(btn_refresh)
        self.load_printer_list()

        return w

    # =========================================================
    # PRINTER CONNECTION & STATUS
    # =========================================================
    def build_connection_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        summary = QFrame()
        summary.setObjectName("SummaryCard")
        summary_layout = QVBoxLayout(summary)
        summary_title = QLabel("Printer health")
        summary_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f3f6fc;")
        self.health_label = QLabel("Checking printer availability…")
        self.health_label.setWordWrap(True)
        self.health_label.setStyleSheet("color: #9eabc0; padding: 4px 0;")
        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(self.health_label)
        summary.setStyleSheet("QFrame#SummaryCard { background: #151c28; border: 1px solid #29354a; border-radius: 12px; }")
        layout.addWidget(summary)

        self.connection_table = QTableWidget(0, 5)
        self.connection_table.setHorizontalHeaderLabels(["Printer", "Driver", "Port", "Status", "Default"])
        self.connection_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.connection_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.connection_table.setSelectionMode(QTableWidget.SingleSelection)
        self.connection_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.connection_table.setAlternatingRowColors(True)
        layout.addWidget(self.connection_table, 1)

        self.connection_details = QTextEdit()
        self.connection_details.setReadOnly(True)
        self.connection_details.setPlaceholderText("Select a printer to view its details.")
        self.connection_details.setMaximumHeight(95)
        layout.addWidget(self.connection_details)

        buttons = QHBoxLayout()
        self.btn_refresh_connection = QPushButton("↻  Refresh")
        self.btn_connect = QPushButton("View Selected")
        self.btn_default = QPushButton("Set as Default")
        self.btn_test = QPushButton("Print Test Page")
        for button in (self.btn_refresh_connection, self.btn_connect, self.btn_default, self.btn_test):
            button.setCursor(Qt.PointingHandCursor)
            buttons.addWidget(button)
        layout.addLayout(buttons)

        self.queue_label = QLabel("Print queue: select a printer to inspect its current status.")
        self.queue_label.setStyleSheet("color: #8995aa; padding: 4px 0;")
        layout.addWidget(self.queue_label)

        self.btn_refresh_connection.clicked.connect(self.load_connection_printers)
        self.connection_table.itemSelectionChanged.connect(self.show_connection_details)
        self.btn_connect.clicked.connect(self.show_selected_printer)
        self.btn_default.clicked.connect(self.set_default_connection_printer)
        self.btn_test.clicked.connect(self.test_connection_printer)
        self.load_connection_printers()
        return page

    def _printer_manager(self):
        from printer.printer_manager import PrinterManager
        return PrinterManager()

    def load_printer_list(self):
        try:
            current = self.printer_list.currentText()
            printers = self._printer_manager().get_printers()
            self.printer_list.clear()
            names = [p.get("name", "") for p in printers if p.get("name")]
            if names:
                self.printer_list.addItems(names)
                default_name = next((p["name"] for p in printers if p.get("default")), "")
                if default_name:
                    self.printer_list.setCurrentText(default_name)
                elif current in names:
                    self.printer_list.setCurrentText(current)
            else:
                self.printer_list.addItem("No printers found")
        except Exception as exc:
            self.printer_list.clear()
            self.printer_list.addItem("Printer service unavailable")
            print(f"Printer refresh failed: {exc}")

    def load_connection_printers(self):
        self.connection_table.setRowCount(0)
        try:
            printers = self._printer_manager().get_printers()
            for printer in printers:
                row = self.connection_table.rowCount()
                self.connection_table.insertRow(row)
                values = [
                    printer.get("name", ""),
                    printer.get("driver", ""),
                    printer.get("port", ""),
                    printer.get("status", "Unknown"),
                    "Yes" if printer.get("default") else "No",
                ]
                for col, value in enumerate(values):
                    self.connection_table.setItem(row, col, QTableWidgetItem(str(value)))
            if printers:
                self.health_label.setText(f"{len(printers)} installed printer(s) detected. Select a printer to inspect its status.")
                self.connection_table.selectRow(0)
            else:
                self.health_label.setText("No printers were returned by Windows. Check that a printer is installed and available.")
                self.connection_details.setPlainText("No printer details available.")
                self.queue_label.setText("Print queue: unavailable")
        except Exception as exc:
            self.health_label.setText("Printer detection is unavailable on this system. This feature requires Windows printer services and pywin32.")
            self.connection_details.setPlainText(str(exc))
            self.queue_label.setText("Print queue: unable to read printer information")

    def _selected_printer_name(self):
        row = self.connection_table.currentRow()
        item = self.connection_table.item(row, 0) if row >= 0 else None
        return item.text() if item else None

    def show_connection_details(self):
        name = self._selected_printer_name()
        if not name:
            return
        try:
            printers = self._printer_manager().get_printers()
            printer = next((p for p in printers if p.get("name") == name), None)
            if not printer:
                return
            details = (
                f"Printer: {printer.get('name', 'Unknown')}    |    "
                f"Status: {printer.get('status', 'Unknown')}\n"
                f"Driver: {printer.get('driver') or 'Not reported'}    |    "
                f"Port: {printer.get('port') or 'Not reported'}    |    "
                f"Default: {'Yes' if printer.get('default') else 'No'}"
            )
            self.connection_details.setPlainText(details)
            self.queue_label.setText(f"Selected printer: {name}  •  Reported status: {printer.get('status', 'Unknown')}")
            status = printer.get("status", "Unknown")
            self.health_label.setText(f"{name} — {status}. Driver and port information are read from the Windows printer configuration.")
        except Exception as exc:
            self.connection_details.setPlainText(f"Could not read printer details: {exc}")

    def show_selected_printer(self):
        name = self._selected_printer_name()
        if not name:
            QMessageBox.information(self, "Select a printer", "Select a printer from the table first.")
            return
        self.show_connection_details()
        QMessageBox.information(self, "Selected printer", f"Selected printer:\n{name}\n\nThis confirms the printer selected in the manager; it does not create a separate hardware connection.")

    def set_default_connection_printer(self):
        name = self._selected_printer_name()
        if not name:
            QMessageBox.information(self, "Select a printer", "Select a printer from the table first.")
            return
        try:
            success = self._printer_manager().set_default(name)
            if success:
                self.load_connection_printers()
                QMessageBox.information(self, "Default printer updated", f"{name} is now the default printer.")
            else:
                QMessageBox.warning(self, "Could not set default", "Windows did not allow the default printer to be changed.")
        except Exception as exc:
            QMessageBox.warning(self, "Printer error", str(exc))

    def test_connection_printer(self):
        name = self._selected_printer_name()
        if not name:
            QMessageBox.information(self, "Select a printer", "Select a printer from the table first.")
            return
        answer = QMessageBox.question(self, "Print test page", f"Send a test print request to:\n{name}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer != QMessageBox.Yes:
            return
        try:
            success = self._printer_manager().print_test_page(name)
            if success:
                QMessageBox.information(self, "Test print requested", f"A test print request was sent for {name}. Check the printer queue for the result.")
            else:
                QMessageBox.warning(self, "Test print failed", "The test print request could not be started. Check the printer and Windows print spooler.")
        except Exception as exc:
            QMessageBox.warning(self, "Test print failed", str(exc))

    def show_page(self, page, button, title, subtitle, animate=True):
        if self.stack.currentWidget() is page:
            self._set_active_nav(button)
            self.page_heading.setText(title)
            self.page_subheading.setText(subtitle)
            return
        self.stack.setCurrentWidget(page)
        self.page_heading.setText(title)
        self.page_subheading.setText(subtitle)
        self._set_active_nav(button)
        if animate:
            effect = QGraphicsOpacityEffect(self.stack)
            self.stack.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity", self)
            animation.setDuration(190)
            animation.setStartValue(0.35)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.finished.connect(lambda: self.stack.setGraphicsEffect(None))
            self._page_animation = animation
            animation.start()

    def _set_active_nav(self, active_button):
        for button in self.nav_buttons:
            button.setProperty("active", button is active_button)
            button.style().unpolish(button)
            button.style().polish(button)

    # =========================================================
    # DESIGNER
    # =========================================================
    def save_template(self):
        """Save the current canvas layout as a JSON template."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Save label template", "label_template.json",
            "Label Templates (*.json)"
        )
        if not path:
            return
        try:
            elements = []
            for item in self.canvas.scene.items():
                if item is self.canvas.label_rect or item.parentItem() is not None:
                    continue
                element = {
                    "type": item.__class__.__name__,
                    "x": float(item.pos().x()),
                    "y": float(item.pos().y()),
                    "rotation": float(item.rotation()),
                    "opacity": float(item.opacity()),
                }
                if hasattr(item, "toPlainText"):
                    element["text"] = item.toPlainText()
                    element["font_size"] = item.font().pointSize()
                elif hasattr(item, "rect"):
                    rect = item.rect()
                    element["width"] = float(rect.width())
                    element["height"] = float(rect.height())
                elif hasattr(item, "pixmap"):
                    element["width"] = item.pixmap().width()
                    element["height"] = item.pixmap().height()
                elements.append(element)
            template = {
                "template_version": 1,
                "name": os.path.splitext(os.path.basename(path))[0],
                "label_size_mm": {
                    "width": self.designer_label_width.value(),
                    "height": self.designer_label_height.value(),
                },
                "elements": elements,
            }
            with open(path, "w", encoding="utf-8") as file:
                json.dump(template, file, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Template saved", f"Template saved to:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", f"Could not save the template:\n{exc}")

    def build_designer(self):
        """
        Redesigned label workspace inspired by professional desktop label editors.
        Keeps the existing Canvas API so mapping/preview workflows continue to use it.
        """
        from ui.widgets.canvas import Canvas
        from ui.widgets.fields_panel import FieldsPanel
        from ui.widgets.properties_panel import PropertiesPanel

        page = QWidget()
        page.setObjectName("DesignerPage")
        root = QVBoxLayout(page)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # --- Designer command bar ---
        command_bar = QFrame()
        command_bar.setObjectName("DesignerCommandBar")
        command_layout = QHBoxLayout(command_bar)
        command_layout.setContentsMargins(10, 7, 10, 7)
        command_layout.setSpacing(6)

        self.designer_title = QLabel("New Design  (40 × 20 mm)")
        self.designer_title.setObjectName("DesignerDocumentTitle")
        command_layout.addWidget(self.designer_title)
        command_layout.addStretch()

        self.designer_undo_btn = QPushButton("↶")
        self.designer_undo_btn.setToolTip("Undo — not available until edit history is implemented")
        self.designer_redo_btn = QPushButton("↷")
        self.designer_redo_btn.setToolTip("Redo — not available until edit history is implemented")
        self.designer_save_btn = QPushButton("▣  Save Template")
        self.designer_print_btn = QPushButton("Continue to Print  →")
        self.designer_reset_btn = QPushButton("⟲  Fit Label")
        for button in (self.designer_undo_btn, self.designer_redo_btn,
                       self.designer_save_btn, self.designer_print_btn,
                       self.designer_reset_btn):
            button.setMinimumHeight(32)
            command_layout.addWidget(button)
        self.designer_undo_btn.setEnabled(False)
        self.designer_redo_btn.setEnabled(False)
        self.designer_save_btn.clicked.connect(self.save_template)
        self.designer_print_btn.clicked.connect(
            lambda: self.show_page(
                self.print_screen, None, "Print Labels",
                "Review the customized label, choose a printer, then print and save."
            )
        )
        root.addWidget(command_bar)

        # --- Three-column workspace ---
        workspace = QHBoxLayout()
        workspace.setSpacing(10)

        # Narrow tool rail, similar to professional label editors.
        tool_rail = QFrame()
        tool_rail.setObjectName("DesignerToolRail")
        tool_rail.setFixedWidth(82)
        rail_layout = QVBoxLayout(tool_rail)
        rail_layout.setContentsMargins(5, 8, 5, 8)
        rail_layout.setSpacing(7)

        rail_specs = [
            ("▣", "Save", "file"),
            ("◇", "Shape", "shapes"),
            ("T", "Text", "text"),
            ("▤", "Data", "data"),
            ("▥", "Barcode", "barcode"),
            ("▦", "QR Code", "qr"),
            ("▧", "Image", "media"),
            ("☷", "Layers", "layers"),
        ]
        self.designer_tool_buttons = {}
        for glyph, label, key in rail_specs:
            btn = QPushButton(f"{glyph}\n{label}")
            btn.setObjectName("DesignerToolButton")
            btn.setMinimumHeight(58)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(label)
            rail_layout.addWidget(btn)
            self.designer_tool_buttons[key] = btn
        rail_layout.addStretch()
        self.designer_tool_buttons["text"].clicked.connect(self._designer_add_text)
        self.designer_tool_buttons["barcode"].clicked.connect(self._designer_add_barcode)
        self.designer_tool_buttons["qr"].clicked.connect(self._designer_add_qr)
        self.designer_tool_buttons["shapes"].clicked.connect(self._designer_add_shape)
        self.designer_tool_buttons["file"].clicked.connect(self.save_template)
        self.designer_tool_buttons["data"].clicked.connect(
            lambda: self.show_page(self.mapping_screen, None, "Field Mapping",
                                   "Map product data to your label elements.")
        )
        self.designer_tool_buttons["media"].clicked.connect(self._designer_add_image)
        self.designer_tool_buttons["layers"].clicked.connect(self._designer_show_layers)
        workspace.addWidget(tool_rail)

        # Left inspector panel with editable properties.
        inspector = QFrame()
        inspector.setObjectName("DesignerInspector")
        inspector.setMinimumWidth(210)
        inspector.setMaximumWidth(255)
        inspector_layout = QVBoxLayout(inspector)
        inspector_layout.setContentsMargins(12, 12, 12, 12)
        inspector_layout.setSpacing(8)

        inspector_header = QLabel("Properties")
        inspector_header.setObjectName("DesignerSectionTitle")
        inspector_layout.addWidget(inspector_header)
        selected_hint = QLabel("Select an element to edit its position and size.")
        selected_hint.setObjectName("DesignerMuted")
        selected_hint.setWordWrap(True)
        inspector_layout.addWidget(selected_hint)

        basics_title = QLabel("BASICS")
        basics_title.setObjectName("DesignerSectionCaption")
        inspector_layout.addWidget(basics_title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)
        self.designer_x = QDoubleSpinBox()
        self.designer_y = QDoubleSpinBox()
        self.designer_width = QDoubleSpinBox()
        self.designer_height = QDoubleSpinBox()
        self.designer_rotation = QSpinBox()
        self.designer_opacity = QSlider(Qt.Horizontal)
        for spin in (self.designer_x, self.designer_y):
            spin.setRange(-10000, 10000)
            spin.setDecimals(1)
        for spin in (self.designer_width, self.designer_height):
            spin.setRange(1, 10000)
            spin.setDecimals(1)
        self.designer_rotation.setRange(-360, 360)
        self.designer_opacity.setRange(10, 100)
        self.designer_opacity.setValue(100)

        prop_fields = [
            ("X (px)", self.designer_x), ("Y (px)", self.designer_y),
            ("Width (px)", self.designer_width), ("Height (px)", self.designer_height),
            ("Rotation", self.designer_rotation),
        ]
        for index, (label, field) in enumerate(prop_fields):
            r, c = divmod(index, 2)
            cell = QVBoxLayout()
            caption = QLabel(label)
            caption.setObjectName("DesignerMuted")
            cell.addWidget(caption)
            cell.addWidget(field)
            grid.addLayout(cell, r, c)
        inspector_layout.addLayout(grid)

        opacity_row = QHBoxLayout()
        opacity_label = QLabel("Opacity")
        opacity_label.setObjectName("DesignerMuted")
        self.designer_opacity_value = QLabel("100%")
        opacity_row.addWidget(opacity_label)
        opacity_row.addStretch()
        opacity_row.addWidget(self.designer_opacity_value)
        inspector_layout.addLayout(opacity_row)
        inspector_layout.addWidget(self.designer_opacity)

        style_title = QLabel("TEXT STYLE")
        style_title.setObjectName("DesignerSectionCaption")
        inspector_layout.addWidget(style_title)
        self.designer_font_size = QSpinBox()
        self.designer_font_size.setRange(5, 96)
        self.designer_font_size.setValue(10)
        self.designer_font_size.setPrefix("Font  ")
        inspector_layout.addWidget(self.designer_font_size)

        self.designer_apply_btn = QPushButton("Apply Properties")
        self.designer_apply_btn.setObjectName("PrimaryButton")
        self.designer_apply_btn.clicked.connect(self._designer_apply_properties)
        inspector_layout.addWidget(self.designer_apply_btn)

        self.designer_delete_btn = QPushButton("Delete Selected")
        self.designer_delete_btn.clicked.connect(self._designer_delete_selected)
        inspector_layout.addWidget(self.designer_delete_btn)
        inspector_layout.addStretch()
        workspace.addWidget(inspector)

        # Main light-gray work area with existing graphics canvas.
        stage = QFrame()
        stage.setObjectName("DesignerStage")
        stage_layout = QVBoxLayout(stage)
        stage_layout.setContentsMargins(10, 10, 10, 8)
        stage_layout.setSpacing(6)

        self.canvas = Canvas()
        self.canvas.setObjectName("LabelCanvas")
        self.canvas.setBackgroundBrush(QBrush(QColor("#e5e7eb")))
        self.canvas.setFrameShape(QFrame.NoFrame)
        self.canvas.setRenderHints(self.canvas.renderHints())
        self.canvas.setDragMode(QGraphicsView.RubberBandDrag)
        self.canvas.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.canvas.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.canvas.setMinimumSize(360, 320)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.set_label_size(400, 200)
        # Scene bounds are managed by Canvas.set_label_size so large and small
        # labels remain fully editable after resizing.
        self.canvas._update_scene_bounds()
        self.canvas.label_rect.setPen(QColor("#111827"))
        self.canvas.label_rect.setZValue(-100)
        stage_layout.addWidget(self.canvas, 1)

        # Bottom bar: physical size, grid/ruler toggles and zoom.
        footer = QFrame()
        footer.setObjectName("DesignerFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(8, 5, 8, 5)
        footer_layout.setSpacing(8)
        footer_layout.addWidget(QLabel("Size:"))
        self.designer_label_width = QDoubleSpinBox()
        self.designer_label_width.setRange(10, 300)
        self.designer_label_width.setValue(40)
        self.designer_label_width.setSuffix(" mm")
        self.designer_label_width.setMaximumWidth(100)
        self.designer_label_height = QDoubleSpinBox()
        self.designer_label_height.setRange(10, 300)
        self.designer_label_height.setValue(20)
        self.designer_label_height.setSuffix(" mm")
        self.designer_label_height.setMaximumWidth(100)
        footer_layout.addWidget(self.designer_label_width)
        footer_layout.addWidget(QLabel("×"))
        footer_layout.addWidget(self.designer_label_height)
        self.designer_grid_toggle = QCheckBox("Grid")
        self.designer_grid_toggle.setChecked(True)
        self.designer_ruler_toggle = QCheckBox("Ruler")
        self.designer_ruler_toggle.setChecked(True)
        footer_layout.addSpacing(12)
        footer_layout.addWidget(self.designer_grid_toggle)
        footer_layout.addWidget(self.designer_ruler_toggle)
        footer_layout.addStretch()
        self.designer_zoom_label = QLabel("100%")
        self.designer_zoom_out = QPushButton("−")
        self.designer_zoom_in = QPushButton("+")
        self.designer_zoom_out.setMaximumWidth(34)
        self.designer_zoom_in.setMaximumWidth(34)
        footer_layout.addWidget(self.designer_zoom_out)
        footer_layout.addWidget(self.designer_zoom_label)
        footer_layout.addWidget(self.designer_zoom_in)
        stage_layout.addWidget(footer)
        workspace.addWidget(stage, 1)

        # Right-hand layer list keeps element selection visible.
        layer_panel = QFrame()
        layer_panel.setObjectName("DesignerLayers")
        layer_panel.setMinimumWidth(145)
        layer_panel.setMaximumWidth(185)
        layer_layout = QVBoxLayout(layer_panel)
        layer_layout.setContentsMargins(10, 12, 10, 10)
        layer_layout.setSpacing(8)
        layer_title = QLabel("Layers")
        layer_title.setObjectName("DesignerSectionTitle")
        layer_layout.addWidget(layer_title)
        self.designer_layers = QTableWidget(0, 1)
        self.designer_layers.setHorizontalHeaderLabels(["Elements"])
        self.designer_layers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.designer_layers.verticalHeader().setVisible(False)
        self.designer_layers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.designer_layers.setSelectionMode(QAbstractItemView.SingleSelection)
        self.designer_layers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._designer_layer_items = []
        layer_layout.addWidget(self.designer_layers, 1)
        refresh_layers = QPushButton("Refresh Layers")
        refresh_layers.clicked.connect(self._designer_refresh_layers)
        layer_layout.addWidget(refresh_layers)
        workspace.addWidget(layer_panel)

        root.addLayout(workspace, 1)

        # Keep existing backend hooks and add selection/property synchronization.
        self.fields = FieldsPanel()
        self.props = PropertiesPanel()
        self.fields.btn_text.clicked.connect(self.canvas.add_text)
        self.fields.btn_barcode.clicked.connect(self.canvas.add_barcode)
        self.fields.btn_qr.clicked.connect(self.canvas.add_qr)
        self.props.apply_btn.clicked.connect(self.update_position)
        self.canvas.scene.selectionChanged.connect(self.update_properties)
        # Selection changes must NOT rebuild the layer table. Rebuilding it
        # during a scene selection callback invalidates row/item mappings.
        self.canvas.scene.selectionChanged.connect(self._designer_sync_layer_selection)
        self.canvas.scene.selectionChanged.connect(self._designer_load_properties)
        self.designer_layers.itemSelectionChanged.connect(self._designer_select_layer)
        self.designer_label_width.valueChanged.connect(self._designer_apply_label_size)
        self.designer_label_height.valueChanged.connect(self._designer_apply_label_size)
        self.designer_grid_toggle.toggled.connect(self._designer_toggle_grid)
        self.designer_ruler_toggle.toggled.connect(self._designer_toggle_rulers)
        self.designer_zoom_in.clicked.connect(lambda: self._designer_zoom(1.15))
        self.designer_zoom_out.clicked.connect(lambda: self._designer_zoom(1 / 1.15))
        self.designer_reset_btn.clicked.connect(self._designer_fit_label)
        self.designer_opacity.valueChanged.connect(
            lambda value: self.designer_opacity_value.setText(f"{value}%")
        )
        self._designer_fit_label()
        self._designer_refresh_layers()
        return page

    def _designer_current_product_record(self):
        """Resolve product data even when Label Designer is opened directly."""
        record = getattr(self, "selected_data", None)
        if isinstance(record, dict) and record:
            return record
        rows = getattr(self, "selected_product_rows", None) or []
        if rows and isinstance(rows[0], dict):
            self.selected_data = rows[0]
            return rows[0]
        table = getattr(self, "table", None)
        fields = getattr(self, "fields_config", None) or []
        if table is not None and fields:
            row = table.currentRow()
            if row < 0 and table.rowCount():
                row = 0
            if row >= 0:
                record = {}
                for col, field in enumerate(fields):
                    cell = table.item(row, col)
                    record[field] = cell.text() if cell else ""
                self.selected_data = record
                self.selected_product_rows = [record]
                return record
        return {}

    def _designer_add_text(self):
        record = self._designer_current_product_record()
        if record:
            preferred = ("NAME", "PRODUCT", "PRODUCT_NAME", "TITLE")
            normalized = {str(k).strip().upper().replace(" ", "_"): v
                          for k, v in record.items()}
            key = next((k for k in preferred if normalized.get(k) not in (None, "")), None)
            if key:
                item = self.canvas.add_text_direct(f"{key}: {normalized[key]}")
            else:
                item = self.canvas.add_text_direct(
                    f"{next(iter(record))}: {next(iter(record.values()))}"
                )
        else:
            item = self.canvas.add_text()
        self._designer_finish_add(item)

    def _designer_default_product_value(self, preferred=("SKU", "BARCODE", "CODE", "PRODUCT_CODE", "EAN", "UPC", "NAME")):
        record = self._designer_current_product_record()
        normalized = {str(k).strip().upper().replace(" ", "_"): v
                      for k, v in record.items()}
        for key in preferred:
            value = normalized.get(key)
            if value not in (None, ""):
                return str(value)
        for value in normalized.values():
            if value not in (None, ""):
                return str(value)
        return "SKU001"

    def _designer_add_barcode(self):
        value = self._designer_default_product_value()
        barcode_type = "CODE128"
        if hasattr(self, "mapping_barcode_type"):
            barcode_type = self.mapping_barcode_type.currentText()
        item = self.canvas.add_barcode_direct(
            value, barcode_type=barcode_type, height=70, scale=1.0, show_text=True
        )
        self._designer_finish_add(item)

    def _designer_add_qr(self):
        value = self._designer_default_product_value(
            ("SKU", "BARCODE", "CODE", "PRODUCT_CODE", "EAN", "UPC", "NAME")
        )
        item = self.canvas.add_qr_direct(value)
        self._designer_finish_add(item)

    def _designer_finish_add(self, item):
        if item is not None:
            # Track every added artwork item explicitly. Never replace the
            # scene or remove previously-created items when a tool is clicked.
            if not hasattr(self, "_designer_artwork_items"):
                self._designer_artwork_items = []
            if item not in self._designer_artwork_items:
                self._designer_artwork_items.append(item)
            if item.scene() is None:
                self.canvas.scene.addItem(item)
            if item.scene() is self.canvas.scene:
                self.canvas.scene.blockSignals(True)
                try:
                    self.canvas.scene.clearSelection()
                    item.setSelected(True)
                finally:
                    self.canvas.scene.blockSignals(False)
                self.canvas.ensureVisible(item, 30, 30)
        self._designer_refresh_layers()
        self._designer_sync_layer_selection()
        self._designer_load_properties()

    def _designer_add_shape(self):
        item = self.canvas.add_shape()
        self._designer_finish_add(item)

    def _designer_add_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Add image to label", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        try:
            item = self.canvas.add_image(path)
            self._designer_finish_add(item)
        except Exception as exc:
            QMessageBox.warning(self, "Image error", str(exc))

    def _designer_show_layers(self):
        self._designer_refresh_layers()
        self.designer_layers.setFocus()

    def _designer_refresh_layers(self, *args):
        """Refresh layer rows only after adding/removing objects, not on selection."""
        if not hasattr(self, "designer_layers") or not hasattr(self, "canvas"):
            return
        from PySide6.QtWidgets import QTableWidgetItem, QGraphicsTextItem, QGraphicsPixmapItem
        table = self.designer_layers
        selected = self.canvas.get_selected_item()
        table.blockSignals(True)
        try:
            table.setRowCount(0)
            self._designer_layer_items = []
            # Scene.items() is top-to-bottom. Keep only top-level artwork;
            # barcode/QR group children are represented by their parent group.
            items = []
            for item in self.canvas.scene.items():
                try:
                    if item is self.canvas.label_rect or item.parentItem() is not None:
                        continue
                    if item.scene() is self.canvas.scene:
                        items.append(item)
                except RuntimeError:
                    continue
            for row, item in enumerate(items):
                marker = item.data(0)
                kind = str(marker).upper() if marker else (
                    "TEXT" if isinstance(item, QGraphicsTextItem) else
                    "IMAGE / BARCODE" if isinstance(item, QGraphicsPixmapItem) else
                    "SHAPE / GROUP"
                )
                cell = QTableWidgetItem(f"{kind}  ·  {row + 1}")
                cell.setData(Qt.UserRole, row)
                table.insertRow(row)
                table.setItem(row, 0, cell)
                self._designer_layer_items.append(item)
                if item is selected or item.isSelected():
                    table.selectRow(row)
                    table.setCurrentCell(row, 0)
        finally:
            table.blockSignals(False)
        self._designer_sync_layer_selection()

    def _designer_sync_layer_selection(self):
        """Highlight the selected canvas item without rebuilding the layer list."""
        if not hasattr(self, "designer_layers"):
            return
        selected = self.canvas.get_selected_item()
        table = self.designer_layers
        table.blockSignals(True)
        try:
            table.clearSelection()
            if selected is not None:
                for row, item in enumerate(getattr(self, "_designer_layer_items", [])):
                    if item is selected and item.scene() is self.canvas.scene:
                        table.selectRow(row)
                        table.setCurrentCell(row, 0)
                        break
            self.designer_delete_btn.setEnabled(selected is not None)
        finally:
            table.blockSignals(False)

    def _designer_select_layer(self):
        row = self.designer_layers.currentRow()
        if row < 0 or row >= len(getattr(self, "_designer_layer_items", [])):
            return
        item = self._designer_layer_items[row]
        if item is None or item.scene() is not self.canvas.scene:
            self._designer_refresh_layers()
            return
        # Block scene callbacks while switching selection so the table remains
        # intact and its row-to-item mapping cannot be replaced mid-click.
        self.canvas.scene.blockSignals(True)
        try:
            self.canvas.scene.clearSelection()
            item.setSelected(True)
        finally:
            self.canvas.scene.blockSignals(False)
        self.canvas.centerOn(item)
        self._designer_load_properties()
        self._designer_sync_layer_selection()
        self.canvas.viewport().update()

    def _designer_load_properties(self):
        item = self.canvas.get_selected_item()
        if item is None:
            self.designer_delete_btn.setEnabled(False)
            return
        from PySide6.QtWidgets import QGraphicsTextItem
        from PySide6.QtCore import QSignalBlocker
        widgets = (
            self.designer_x, self.designer_y, self.designer_width,
            self.designer_height, self.designer_rotation,
            self.designer_font_size, self.designer_opacity
        )
        blockers = [QSignalBlocker(widget) for widget in widgets]
        pos = item.pos()
        self.designer_x.setValue(pos.x())
        self.designer_y.setValue(pos.y())
        bounds = item.sceneBoundingRect()
        self.designer_width.setValue(max(1.0, bounds.width()))
        self.designer_height.setValue(max(1.0, bounds.height()))
        self.designer_rotation.setValue(int(round(item.rotation())))
        if isinstance(item, QGraphicsTextItem):
            point_size = item.font().pointSizeF()
            self.designer_font_size.setValue(
                max(5, int(round(point_size if point_size > 0 else 10)))
            )
        self.designer_opacity.setValue(round(item.opacity() * 100))
        del blockers
        self.designer_delete_btn.setEnabled(True)

    def _designer_apply_properties(self):
        item = self.canvas.get_selected_item()
        if item is None:
            QMessageBox.information(self, "Select an element", "Select a label element before applying properties.")
            return
        from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsRectItem, QGraphicsPixmapItem
        from PySide6.QtGui import QTransform

        item.setPos(self.designer_x.value(), self.designer_y.value())
        item.setRotation(self.designer_rotation.value())
        width = float(self.designer_width.value())
        height = float(self.designer_height.value())

        if isinstance(item, QGraphicsTextItem):
            font = item.font()
            font.setPointSizeF(float(self.designer_font_size.value()))
            item.setFont(font)
            item.setTextWidth(width)
        elif isinstance(item, QGraphicsRectItem):
            rect = item.rect()
            item.setTransform(QTransform())
            item.setScale(1.0)
            item.setRect(rect.x(), rect.y(), width, height)
        elif isinstance(item, QGraphicsPixmapItem):
            pix = item.pixmap()
            if pix.width() > 0 and pix.height() > 0:
                item.setTransformOriginPoint(0, 0)
                item.setScale(1.0)
                item.setTransform(QTransform.fromScale(
                    width / pix.width(), height / pix.height()
                ))
        else:
            self.canvas.resize_item(item, width, height)

        item.setOpacity(self.designer_opacity.value() / 100.0)
        self.canvas._update_scene_bounds()
        self._designer_load_properties()
        self.canvas.viewport().update()

    def _designer_delete_selected(self):
        item = self.canvas.get_selected_item()
        if not item:
            return
        self.canvas.scene.blockSignals(True)
        try:
            self.canvas.scene.removeItem(item)
        finally:
            self.canvas.scene.blockSignals(False)
        self.canvas._update_scene_bounds()
        self._designer_refresh_layers()
        self.designer_delete_btn.setEnabled(False)

    def _designer_apply_label_size(self, *args):
        width_mm = self.designer_label_width.value()
        height_mm = self.designer_label_height.value()
        # Canvas coordinates use 10 px per mm in the current designer.
        self.canvas.set_label_size(int(width_mm * 10), int(height_mm * 10))
        self.designer_title.setText(f"New Design  ({width_mm:g} × {height_mm:g} mm)")
        self._designer_fit_label()

    def _designer_toggle_grid(self, enabled):
        if hasattr(self.canvas, "set_grid_enabled"):
            self.canvas.set_grid_enabled(enabled)
        self.canvas.viewport().update()

    def _designer_toggle_rulers(self, enabled):
        self.canvas.set_rulers_enabled(enabled)
        self.designer_ruler_toggle.setToolTip(
            "Ruler guides enabled" if enabled else "Ruler guides hidden"
        )

    def _designer_zoom(self, factor):
        current = self.canvas.transform().m11()
        target = max(0.15, min(5.0, current * float(factor)))
        if current > 0:
            self.canvas.scale(target / current, target / current)
        self.designer_zoom_label.setText(f"{int(target * 100)}%")

    def _designer_fit_label(self):
        # Defer until Qt has laid out the stage; fit only the paper, never the
        # changing union of paper + objects (which caused the label to jump away).
        from PySide6.QtCore import QTimer
        def apply_fit():
            if (not hasattr(self, "canvas") or self.canvas.label_rect is None
                    or self.canvas.label_rect.scene() is not self.canvas.scene):
                return
            rect = self.canvas.label_rect.sceneBoundingRect()
            if rect.width() <= 0 or rect.height() <= 0:
                return
            self.canvas.resetTransform()
            self.canvas.fitInView(rect.adjusted(-8, -8, 8, 8), Qt.KeepAspectRatio)
            self.canvas.centerOn(rect.center())
            self.designer_zoom_label.setText(f"{int(self.canvas.transform().m11() * 100)}%")
        QTimer.singleShot(0, apply_fit)

    # =========================================================
    # POSITION
    # =========================================================
    def update_position(self):

        try:

            x = int(self.props.x_input.text())
            y = int(self.props.y_input.text())

            self.canvas.set_position(x, y)

        except:
            print("Invalid Position")

    def update_properties(self):

        x, y = self.canvas.get_position()

        if x is not None:

            self.props.x_input.setText(str(x))
            self.props.y_input.setText(str(y))
    

    def build_database_screen(self):
        """Allow each Windows computer to configure its own SQL Server connection."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        intro = QLabel("Enter the SQL Server details for this computer. Test the connection before saving.")
        intro.setWordWrap(True)
        intro.setObjectName("MetricHint")
        layout.addWidget(intro)

        form_panel = QFrame()
        form_panel.setObjectName("Panel")
        form = QGridLayout(form_panel)
        form.setContentsMargins(18, 18, 18, 18)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(12)

        self.sql_driver = QComboBox()
        try:
            import pyodbc
            self.sql_driver.addItems(sorted(pyodbc.drivers()))
        except Exception:
            self.sql_driver.addItems(["SQL Server", "ODBC Driver 17 for SQL Server", "ODBC Driver 18 for SQL Server"])
        self.sql_server = QLineEdit(".\\SQLEXPRESS")
        self.sql_database = QLineEdit("barcode_system")
        self.sql_auth = QComboBox()
        self.sql_auth.addItems(["Windows", "SQL Server"])
        self.sql_username = QLineEdit()
        self.sql_password = QLineEdit()
        self.sql_password.setEchoMode(QLineEdit.Password)
        self.sql_trust = QCheckBox("Trust server certificate (useful for local SQL Server installations)")
        self.sql_trust.setChecked(True)

        fields = [
            ("ODBC Driver", self.sql_driver), ("Server / Instance", self.sql_server),
            ("Database", self.sql_database), ("Authentication", self.sql_auth),
            ("SQL Username", self.sql_username), ("SQL Password", self.sql_password),
        ]
        for row, (caption, widget) in enumerate(fields):
            form.addWidget(QLabel(caption), row, 0)
            form.addWidget(widget, row, 1)
        form.addWidget(self.sql_trust, len(fields), 0, 1, 2)
        layout.addWidget(form_panel)

        self.sql_auth.currentTextChanged.connect(self._update_sql_auth_fields)
        self._update_sql_auth_fields(self.sql_auth.currentText())

        buttons = QHBoxLayout()
        self.sql_test_button = QPushButton("Test Connection")
        self.sql_test_button.setObjectName("PrimaryButton")
        self.sql_save_button = QPushButton("Save Settings")
        self.sql_test_button.clicked.connect(self.test_database_settings)
        self.sql_save_button.clicked.connect(self.save_database_settings)
        buttons.addWidget(self.sql_test_button)
        buttons.addWidget(self.sql_save_button)
        buttons.addStretch()
        layout.addLayout(buttons)

        self.sql_settings_status = QLabel("Connection settings are stored separately for each Windows user.")
        self.sql_settings_status.setWordWrap(True)
        self.sql_settings_status.setObjectName("MetricHint")
        layout.addWidget(self.sql_settings_status)
        layout.addStretch()
        self.load_database_settings_into_form()
        return page

    def _update_sql_auth_fields(self, mode):
        sql_auth = mode == "SQL Server"
        self.sql_username.setEnabled(sql_auth)
        self.sql_password.setEnabled(sql_auth)

    def _collect_sql_settings(self):
        return {
            "driver": self.sql_driver.currentText().strip(),
            "server": self.sql_server.text().strip(),
            "database": self.sql_database.text().strip(),
            "authentication": self.sql_auth.currentText(),
            "username": self.sql_username.text().strip(),
            "password": self.sql_password.text(),
            "trust_server_certificate": self.sql_trust.isChecked(),
        }

    def load_database_settings_into_form(self):
        try:
            from database.connection_settings import load_connection_settings
            settings = load_connection_settings()
            driver_index = self.sql_driver.findText(settings.get("driver", "SQL Server"))
            if driver_index < 0 and settings.get("driver"):
                self.sql_driver.addItem(settings["driver"])
                driver_index = self.sql_driver.findText(settings["driver"])
            if driver_index >= 0:
                self.sql_driver.setCurrentIndex(driver_index)
            self.sql_server.setText(settings.get("server", ".\\SQLEXPRESS"))
            self.sql_database.setText(settings.get("database", "barcode_system"))
            self.sql_auth.setCurrentText(settings.get("authentication", "Windows"))
            self.sql_username.setText(settings.get("username", ""))
            self.sql_password.setText(settings.get("password", ""))
            self.sql_trust.setChecked(settings.get("trust_server_certificate", True))
        except Exception as exc:
            self.sql_settings_status.setText(f"Could not load saved connection settings: {exc}")

    def test_database_settings(self):
        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager(self._collect_sql_settings())
            result = db.test()
            self.sql_settings_status.setText(
                f"Connected successfully. Server: {result[0]} | Database: {result[1]}"
            )
            QMessageBox.information(self, "SQL Server Connected",
                f"Connection successful.\nServer: {result[0]}\nDatabase: {result[1]}\n\nRequired application tables were checked/created.")
        except Exception as exc:
            self.sql_settings_status.setText(f"Connection failed: {exc}")
            QMessageBox.critical(self, "SQL Connection Failed", str(exc))
        finally:
            if db:
                db.close()

    def save_database_settings(self):
        db = None
        try:
            settings = self._collect_sql_settings()
            # Verify the target before making it the active saved connection.
            from database.sql_manager import SQLManager
            db = SQLManager(settings)
            result = db.test()
            from database.connection_settings import save_connection_settings
            save_connection_settings(settings)
            self.sql_settings_status.setText(
                f"Settings saved. Connected to {result[0]} / {result[1]}."
            )
            QMessageBox.information(self, "Settings Saved",
                "SQL Server settings have been saved for this Windows user. All SQL features will use this connection.")
        except Exception as exc:
            self.sql_settings_status.setText(f"Settings were not saved: {exc}")
            QMessageBox.critical(self, "Could Not Save Settings", str(exc))
        finally:
            if db:
                db.close()

    def build_history_screen(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("Print activity")
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        self.history_table = QTableWidget(0, 8)
        self.history_table.setHorizontalHeaderLabels([
            "ID", "Product", "SKU", "Price", "Qty", "Printer", "Copies", "Printed At"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_status = QLabel("History loads from SQL Server when this page opens.")
        self.history_status.setObjectName("MetricHint")
        btn_refresh = QPushButton("↻  Refresh History")
        btn_refresh.clicked.connect(self.load_sql_history)
        layout.addWidget(title)
        layout.addWidget(self.history_status)
        layout.addWidget(self.history_table, 1)
        layout.addWidget(btn_refresh)
        return page

    def open_history_page(self):
        self.show_page(
            self.history_screen, self.btn_history,
            "SQL History", "Review recorded print activity from SQL Server."
        )
        self.load_sql_history()

    def load_sql_history(self):
        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager()
            rows = db.get_history()
            self.history_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data[:8]):
                    self.history_table.setItem(
                        row_idx, col_idx,
                        QTableWidgetItem("" if value is None else str(value))
                    )
            self.history_status.setText(f"{len(rows)} record(s) loaded from SQL Server.")
        except Exception as exc:
            self.history_status.setText("Could not connect to SQL Server. Check database settings and network access.")
            QMessageBox.warning(self, "SQL history unavailable", str(exc))
        finally:
            if db:
                try:
                    db.close()
                except Exception:
                    pass


        # =========================================================
        # TOOLBAR
        # =========================================================
    def init_toolbar(self):

        toolbar = QToolBar()

        self.addToolBar(toolbar)

        save = QAction("Save Template", self)

        toolbar.addAction(save)


# =========================================================
# RUN APP
# =========================================================
def run_app():

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    win = MainWindow()

    win.show()

    sys.exit(app.exec())