from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class FieldsPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.btn_text = QPushButton("Add Text")
        self.btn_barcode = QPushButton("Add Barcode")
        self.btn_qr = QPushButton("Add QR Code")
        
        layout.addWidget(self.btn_qr)
        layout.addWidget(self.btn_text)
        layout.addWidget(self.btn_barcode)
        layout.addStretch()