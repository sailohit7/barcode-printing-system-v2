from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsRectItem,
    QGraphicsItem
)
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtCore import Qt


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Label background
        self.label_rect = QGraphicsRectItem(0, 0, 400, 250)
        self.label_rect.setBrush(QBrush(QColor("white")))
        self.scene.addItem(self.label_rect)

    # =========================
    # NORMAL ADD (BUTTON)
    # =========================
    def add_text(self):
        item = QGraphicsTextItem("Double click to edit")

        item.setDefaultTextColor(QColor("black"))

        font = QFont()
        font.setPointSize(10)
        item.setFont(font)

        item.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )

        item.setPos(50, 50)
        self.scene.addItem(item)

    def add_barcode(self):
        rect = QGraphicsRectItem(0, 0, 140, 50)
        rect.setBrush(QBrush(QColor("black")))

        rect.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )

        rect.setPos(50, 100)
        self.scene.addItem(rect)

        text = QGraphicsTextItem("123456")
        text.setDefaultTextColor(QColor("black"))

        text.setParentItem(rect)
        text.setPos(0, 55)

    def add_qr(self):
        rect = QGraphicsRectItem(0, 0, 80, 80)
        rect.setBrush(QBrush(QColor("black")))

        rect.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )

        rect.setPos(200, 100)
        self.scene.addItem(rect)

        text = QGraphicsTextItem("QR")
        text.setDefaultTextColor(QColor("white"))

        text.setParentItem(rect)
        text.setPos(20, 25)

    # =========================
    # ✅ DIRECT ADD (USED BY MAPPING)
    # =========================
    def add_text_direct(self, text):
        item = QGraphicsTextItem(text)

        item.setDefaultTextColor(QColor("black"))

        font = QFont()
        font.setPointSize(10)
        item.setFont(font)

        item.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )

        self.scene.addItem(item)
        return item

    def add_barcode_direct(
        self, value, barcode_type="CODE128", height=70, scale=1.0, show_text=True
    ):
        """Create a movable barcode image using user-selected format and sizing."""
        import os
        import barcode
        from barcode.writer import ImageWriter
        from PySide6.QtGui import QPixmap
        from PySide6.QtWidgets import QGraphicsPixmapItem

        normalized_type = str(barcode_type).strip().lower()
        type_map = {
            "code128": "code128",
            "code39": "code39",
            "ean13": "ean13",
        }
        if normalized_type not in type_map:
            raise ValueError(f"Unsupported barcode type: {barcode_type}")

        clean_value = str(value).strip()
        if not clean_value:
            raise ValueError("Barcode value cannot be empty.")
        if normalized_type == "ean13":
            if not clean_value.isdigit() or len(clean_value) not in (12, 13):
                raise ValueError("EAN-13 requires a numeric 12-digit value (or 13 digits including checksum).")

        filename = os.path.abspath("temp_barcode_custom")
        writer = ImageWriter()
        code = barcode.get(type_map[normalized_type], clean_value, writer=writer)
        options = {
            "module_height": max(8.0, float(height) / 10.0),
            "module_width": 0.20,
            "write_text": bool(show_text),
            "quiet_zone": 2.0,
            "font_size": 10,
            "text_distance": 2.0,
        }
        saved_path = code.save(filename, options=options)
        pixmap = QPixmap(saved_path)
        if pixmap.isNull():
            raise RuntimeError("Barcode image could not be loaded.")
        item = QGraphicsPixmapItem(pixmap)
        item.setScale(max(0.25, min(3.0, float(scale))))
        item.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable
        )
        self.scene.addItem(item)
        return item

    def add_qr_direct(self, value):
     import qrcode
     from PySide6.QtGui import QPixmap
     from PySide6.QtWidgets import QGraphicsPixmapItem

     img = qrcode.make(value)
     img.save("temp_qr.png")

     pixmap = QPixmap("temp_qr.png")

     item = QGraphicsPixmapItem(pixmap)
     item.setFlags(
        QGraphicsItem.ItemIsMovable |
        QGraphicsItem.ItemIsSelectable
    )

     self.scene.addItem(item)
     return item

    # =========================
    # SELECTION + POSITION
    # =========================
    def get_selected_item(self):
        items = self.scene.selectedItems()
        return items[0] if items else None

    def set_position(self, x, y):
        item = self.get_selected_item()
        if item:
            item.setPos(x, y)

    def get_position(self):
        item = self.get_selected_item()
        if item:
            pos = item.pos()
            return int(pos.x()), int(pos.y())
        return None, None

    # =========================
    # CLEAR CANVAS
    # =========================
    def clear_canvas(self):
        self.scene.clear()

        # redraw label
        self.label_rect = QGraphicsRectItem(0, 0, 400, 250)
        self.label_rect.setBrush(QBrush(QColor("white")))
        self.scene.addItem(self.label_rect)

    # =========================
    # LABEL SIZE
    # =========================
    def set_label_size(self, w, h):
        self.label_rect.setRect(0, 0, w, h)