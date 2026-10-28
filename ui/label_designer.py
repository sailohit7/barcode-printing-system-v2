from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton
)

from ui.widgets.canvas import Canvas
from ui.widgets.fields_panel import FieldsPanel
from ui.widgets.properties_panel import PropertiesPanel

import json


class LabelDesigner(QWidget):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # Layouts
        # -----------------------------
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # -----------------------------
        # Panels
        # -----------------------------
        self.fields_panel = FieldsPanel()
        self.canvas = Canvas()
        self.properties_panel = PropertiesPanel()

        # Add panels to top layout
        top_layout.addWidget(self.fields_panel, 1)
        top_layout.addWidget(self.canvas, 3)
        top_layout.addWidget(self.properties_panel, 1)

        main_layout.addLayout(top_layout)

        # -----------------------------
        # Bottom Buttons
        # -----------------------------
        self.save_btn = QPushButton("Save Template")
        self.save_btn.setFixedHeight(40)
        self.save_btn.clicked.connect(self.save_template)

        main_layout.addWidget(self.save_btn)

        self.setLayout(main_layout)

        # -----------------------------
        # Connections
        # -----------------------------
        self.connect_fields()

        # Canvas → Properties Sync
        self.canvas.on_select = self.properties_panel.load_element

    # --------------------------------
    # Connect field buttons
    # --------------------------------
    def connect_fields(self):

        for btn in self.fields_panel.buttons:
            btn.clicked.connect(self.handle_field_click)

    # --------------------------------
    # Add element to canvas
    # --------------------------------
    def handle_field_click(self):

        sender = self.sender()

        if not sender:
            return

        field_data = sender.field_data

        self.canvas.add_element(field_data)

    # --------------------------------
    # Save template to JSON
    # --------------------------------
    def save_template(self):

        template = {
            "size": {
                "width_mm": 100,
                "height_mm": 70
            },
            "fields": []
        }

        for el in self.canvas.elements:

            field = {
                "type": el["type"],
                "key": el["key"],
                "label": el["label"],
                "x": el["x"],
                "y": el["y"]
            }

            # Add barcode type if needed
            if el["type"] == "barcode":
                field["barcode_type"] = "CODE128"

            template["fields"].append(field)

        # Save to file
        with open("templates/custom_template.json", "w") as f:
            json.dump(template, f, indent=4)

        print("✅ Template saved successfully!")