from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class PropertiesPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("X"))
        self.x_input = QLineEdit()
        layout.addWidget(self.x_input)

        layout.addWidget(QLabel("Y"))
        self.y_input = QLineEdit()
        layout.addWidget(self.y_input)

        layout.addWidget(QLabel("Font Size"))
        self.size_input = QLineEdit()
        layout.addWidget(self.size_input)

        self.apply_btn = QPushButton("Apply")
        layout.addWidget(self.apply_btn)

        layout.addStretch()