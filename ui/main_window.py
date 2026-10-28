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

        self.nav_buttons = [
            self.btn_dashboard, self.btn_designer, self.btn_printer,
            self.btn_connection, self.btn_history
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

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.designer)
        self.stack.addWidget(self.mapping_screen)
        self.stack.addWidget(self.print_screen)
        self.stack.addWidget(self.printer_screen)
        self.stack.addWidget(self.connection_screen)
        self.stack.addWidget(self.history_screen)
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
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
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
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Select a product", "Select a product row in the table before saving history.")
            return
        data = {}
        for col, field in enumerate(self.fields_config):
            item = self.table.item(row, col)
            data[str(field).strip().lower()] = item.text() if item else ""
        db = None
        try:
            from database.sql_manager import SQLManager
            db = SQLManager()
            db.save_print_history(data)
            QMessageBox.information(self, "History saved", "The selected product record was saved to SQL Server print history.")
            if hasattr(self, "history_table"):
                self.load_sql_history()
        except Exception as exc:
            QMessageBox.warning(self, "SQL Server unavailable", f"Could not save history. Check the SQL Server connection and PrintHistory table.\n\n{exc}")
        finally:
            if db:
                try:
                    db.close()
                except Exception:
                    pass

        # =========================================================
        # MAPPING SCREEN
        # =========================================================
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

        row = self.table.currentRow()

        if row < 0:
            print("Select a row first ❌")
            return

        self.selected_data = {}

        for col, field in enumerate(self.fields_config):

            item = self.table.item(row, col)

            self.selected_data[field] = (
                item.text() if item else ""
            )

        self.load_mapping_ui()

        self.stack.setCurrentWidget(
            self.mapping_screen
        )

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
        self.print_summary.setText(f"Product: {name or '—'}    |    SKU / Barcode: {sku or '—'}")

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

    def handle_print(self):
        raw_copies = self.copies_input.text().strip() or "1"
        try:
            copies = int(raw_copies)
            if copies < 1 or copies > 10000:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid copies", "Enter a whole number from 1 to 10000.")
            return
        if not getattr(self, "selected_data", None):
            QMessageBox.information(self, "No product selected", "Return to Dashboard and select a product first.")
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
            normalized = {str(k).strip().casefold(): v for k, v in self.selected_data.items()}
            db.save_print({
                "name": normalized.get("name", normalized.get("product", normalized.get("product_name", ""))),
                "sku": normalized.get("sku", normalized.get("barcode", normalized.get("product_code", ""))),
                "price": normalized.get("price", ""),
                "qty": normalized.get("qty", normalized.get("quantity", "")),
            }, printer_name, copies)
            self.print_status_label.setText(f"Print job submitted to {printer_name}; {copies} copy/copies recorded in SQL Server.")
            QMessageBox.information(self, "Print submitted",
                f"Label sent to {printer_name} for {copies} copy/copies. Print history was saved to SQL Server.")
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
        tool_rail.setFixedWidth(66)
        rail_layout = QVBoxLayout(tool_rail)
        rail_layout.setContentsMargins(5, 8, 5, 8)
        rail_layout.setSpacing(7)

        rail_specs = [
            ("▣", "File", "file"),
            ("◇", "Shapes", "shapes"),
            ("T", "Text", "text"),
            ("▤", "Data", "data"),
            ("▥", "Barcode", "barcode"),
            ("▦", "QR Code", "qr"),
            ("▧", "Media", "media"),
            ("☷", "Layers", "layers"),
        ]
        self.designer_tool_buttons = {}
        for glyph, label, key in rail_specs:
            btn = QPushButton(f"{glyph}\n{label}")
            btn.setObjectName("DesignerToolButton")
            btn.setMinimumHeight(52)
            btn.setCursor(Qt.PointingHandCursor)
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
        self.canvas.scene.setSceneRect(-120, -100, 640, 400)
        self.canvas.label_rect.setPen(QColor("#111827"))
        self.canvas.label_rect.setZValue(-10)
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
        self.designer_layers.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        self.canvas.scene.selectionChanged.connect(self._designer_refresh_layers)
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

    def _designer_add_text(self):
        self.canvas.add_text()
        self._designer_refresh_layers()

    def _designer_add_barcode(self):
        self.canvas.add_barcode()
        self._designer_refresh_layers()

    def _designer_add_qr(self):
        self.canvas.add_qr()
        self._designer_refresh_layers()

    def _designer_add_shape(self):
        from PySide6.QtWidgets import QGraphicsRectItem
        from PySide6.QtGui import QBrush, QColor, QPen
        from PySide6.QtWidgets import QGraphicsItem
        item = QGraphicsRectItem(0, 0, 100, 55)
        item.setBrush(QBrush(QColor("#dbeafe")))
        item.setPen(QPen(QColor("#2563eb"), 2))
        item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        item.setPos(70, 65)
        self.canvas.scene.addItem(item)
        self._designer_refresh_layers()

    def _designer_add_image(self):
        from PySide6.QtWidgets import QGraphicsPixmapItem
        path, _ = QFileDialog.getOpenFileName(
            self, "Add image to label", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not path:
            return
        from PySide6.QtGui import QPixmap
        pixmap = QPixmap(path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Image error", "The selected image could not be loaded.")
            return
        item = QGraphicsPixmapItem(pixmap)
        item.setFlags(item.flags() | item.GraphicsItemFlag.ItemIsMovable |
                      item.GraphicsItemFlag.ItemIsSelectable)
        self.canvas.scene.addItem(item)
        self._designer_refresh_layers()

    def _designer_show_layers(self):
        self._designer_refresh_layers()
        self.designer_layers.setFocus()

    def _designer_refresh_layers(self, *args):
        if not hasattr(self, "designer_layers") or not hasattr(self, "canvas"):
            return
        self.designer_layers.blockSignals(True)
        self.designer_layers.setRowCount(0)
        for item in self.canvas.scene.items():
            if item is self.canvas.label_rect or item.parentItem() is not None:
                continue
            row = self.designer_layers.rowCount()
            self.designer_layers.insertRow(row)
            kind = "Text" if item.__class__.__name__ == "QGraphicsTextItem" else (
                "Barcode / QR" if item.__class__.__name__ in ("QGraphicsPixmapItem",) else "Shape / Code"
            )
            label = f"{kind}  ·  {row + 1}"
            from PySide6.QtWidgets import QTableWidgetItem
            cell = QTableWidgetItem(label)
            cell.setData(Qt.UserRole, item)
            self.designer_layers.setItem(row, 0, cell)
            if item.isSelected():
                self.designer_layers.selectRow(row)
        self.designer_layers.blockSignals(False)

    def _designer_select_layer(self):
        row = self.designer_layers.currentRow()
        if row < 0:
            return
        cell = self.designer_layers.item(row, 0)
        if cell:
            item = cell.data(Qt.UserRole)
            self.canvas.scene.clearSelection()
            if item:
                item.setSelected(True)
                self.canvas.centerOn(item)

    def _designer_load_properties(self):
        item = self.canvas.get_selected_item()
        if not item:
            return
        pos = item.pos()
        self.designer_x.setValue(pos.x())
        self.designer_y.setValue(pos.y())
        rect = item.boundingRect()
        self.designer_width.setValue(max(1, rect.width()))
        self.designer_height.setValue(max(1, rect.height()))
        self.designer_rotation.setValue(int(item.rotation()))
        self._designer_refresh_layers()

    def _designer_apply_properties(self):
        item = self.canvas.get_selected_item()
        if not item:
            QMessageBox.information(self, "Select an element", "Select a label element before applying properties.")
            return
        item.setPos(self.designer_x.value(), self.designer_y.value())
        item.setRotation(self.designer_rotation.value())
        from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsRectItem, QGraphicsPixmapItem
        from PySide6.QtGui import QFont
        if isinstance(item, QGraphicsTextItem):
            font = item.font()
            font.setPointSize(self.designer_font_size.value())
            item.setFont(font)
        elif isinstance(item, QGraphicsRectItem):
            rect = item.rect()
            rect.setWidth(self.designer_width.value())
            rect.setHeight(self.designer_height.value())
            item.setRect(rect)
        elif isinstance(item, QGraphicsPixmapItem):
            bounds = item.pixmap().size()
            if bounds.width() and bounds.height():
                item.setScale(min(self.designer_width.value() / bounds.width(),
                                  self.designer_height.value() / bounds.height()))
        if hasattr(item, "setOpacity"):
            item.setOpacity(self.designer_opacity.value() / 100.0)
        self._designer_refresh_layers()
        self.canvas.viewport().update()

    def _designer_delete_selected(self):
        item = self.canvas.get_selected_item()
        if not item:
            return
        self.canvas.scene.removeItem(item)
        self._designer_refresh_layers()

    def _designer_apply_label_size(self, *args):
        width_mm = self.designer_label_width.value()
        height_mm = self.designer_label_height.value()
        # Canvas coordinates use 10 px per mm in the current designer.
        self.canvas.set_label_size(int(width_mm * 10), int(height_mm * 10))
        self.designer_title.setText(f"New Design  ({width_mm:g} × {height_mm:g} mm)")
        self._designer_fit_label()

    def _designer_toggle_grid(self, enabled):
        if enabled:
            self.canvas.setBackgroundBrush(QBrush(QColor("#e5e7eb")))
            self.canvas.setStyleSheet("""
                QGraphicsView {
                    background-color: #e5e7eb;
                    background-image: none;
                    border: 1px solid #cbd5e1;
                }
            """)
        else:
            self.canvas.setStyleSheet("QGraphicsView { background-color: #e5e7eb; border: 1px solid #cbd5e1; }")

    def _designer_toggle_rulers(self, enabled):
        # Ruler toggle currently controls the visible ruler/grid guide treatment.
        self.designer_ruler_toggle.setToolTip(
            "Ruler guides enabled" if enabled else "Ruler guides hidden"
        )

    def _designer_zoom(self, factor):
        self.canvas.scale(factor, factor)
        self.designer_zoom_label.setText(f"{int(self.canvas.transform().m11() * 100)}%")

    def _designer_fit_label(self):
        self.canvas.resetTransform()
        self.canvas.fitInView(self.canvas.label_rect, Qt.KeepAspectRatio)
        self.designer_zoom_label.setText(f"{int(self.canvas.transform().m11() * 100)}%")
        self.canvas.centerOn(self.canvas.label_rect)

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