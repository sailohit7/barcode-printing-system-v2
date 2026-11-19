from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem,
    QGraphicsItem, QGraphicsPixmapItem
)
from PySide6.QtGui import (
    QBrush, QColor, QFont, QPen, QPainter, QPixmap, QImage, QTransform
)
from PySide6.QtCore import Qt, QRectF
import os
import tempfile


class EditableTextItem(QGraphicsTextItem):
    """Movable text; single click selects, double click edits."""
    def mousePressEvent(self, event):
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setFocus(Qt.FocusReason.MouseFocusReason)
        super().mouseDoubleClickEvent(event)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        super().focusOutEvent(event)


class Canvas(QGraphicsView):
    """
    Stable label editor canvas.
    Every visible artwork object is one top-level scene item. Adding/selecting
    an item never clears or reconstructs existing artwork.
    """
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setBackgroundBrush(QBrush(QColor("#e5e7eb")))
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.grid_enabled = True
        self.rulers_enabled = True
        self.grid_size = 10
        self.label_rect = None
        self._create_label(400, 200)

    def _create_label(self, width, height):
        self.label_rect = QGraphicsRectItem(0, 0, float(width), float(height))
        self.label_rect.setBrush(QBrush(QColor("white")))
        self.label_rect.setPen(QPen(QColor("#64748b"), 1))
        self.label_rect.setZValue(-100000)
        self.label_rect.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        self.label_rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.label_rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.scene.addItem(self.label_rect)
        self._set_scene_bounds()

    def _set_scene_bounds(self):
        if self.label_rect is None or self.label_rect.scene() is not self.scene:
            return
        paper = self.label_rect.rect()
        margin = max(300.0, max(paper.width(), paper.height()))
        self.scene.setSceneRect(paper.adjusted(-margin, -margin, margin, margin))
        self.viewport().update()

    def _update_scene_bounds(self):
        # Kept for compatibility with the rest of the application.
        # The scene rectangle is deliberately independent of selected objects.
        self._set_scene_bounds()

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        if self.label_rect is None:
            return
        paper = self.label_rect.sceneBoundingRect()
        visible = rect.intersected(paper)
        if visible.isEmpty():
            return
        if self.grid_enabled:
            step = max(5, int(self.grid_size))
            painter.save()
            painter.setPen(QPen(QColor("#e9edf2"), 0))
            x = int(visible.left()) - (int(visible.left()) % step)
            while x <= visible.right():
                painter.drawLine(x, visible.top(), x, visible.bottom())
                x += step
            y = int(visible.top()) - (int(visible.top()) % step)
            while y <= visible.bottom():
                painter.drawLine(visible.left(), y, visible.right(), y)
                y += step
            painter.restore()

    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)
        if not self.rulers_enabled or self.label_rect is None:
            return
        paper = self.label_rect.sceneBoundingRect()
        painter.save()
        painter.setPen(QPen(QColor("#64748b"), 0))
        step = 10
        x = int(paper.left())
        while x <= int(paper.right()):
            tick = 7 if (x - int(paper.left())) % 50 == 0 else 3
            painter.drawLine(x, paper.top(), x, paper.top() + tick)
            x += step
        y = int(paper.top())
        while y <= int(paper.bottom()):
            tick = 7 if (y - int(paper.top())) % 50 == 0 else 3
            painter.drawLine(paper.left(), y, paper.left() + tick, y)
            y += step
        painter.restore()

    def set_grid_enabled(self, enabled):
        self.grid_enabled = bool(enabled)
        self.viewport().update()

    def set_rulers_enabled(self, enabled):
        self.rulers_enabled = bool(enabled)
        self.viewport().update()

    def _prepare_item(self, item, kind):
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        item.setData(0, kind)
        item.setZValue(10 + len(self.scene.items()))
        return item

    def _add_item(self, item, kind, x=20, y=20):
        self._prepare_item(item, kind)
        self.scene.addItem(item)
        item.setPos(float(x), float(y))
        self.scene.clearSelection()
        item.setSelected(True)
        self.viewport().update()
        return item

    def add_text(self):
        item = EditableTextItem("Double click to edit")
        item.setDefaultTextColor(QColor("#111827"))
        item.setFont(QFont("Arial", 10))
        item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        return self._add_item(item, "text", 20, 20)

    def add_text_direct(self, text):
        item = EditableTextItem(str(text))
        item.setDefaultTextColor(QColor("#111827"))
        item.setFont(QFont("Arial", 10))
        item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        return self._add_item(item, "text", 20, 20)

    def _barcode_pixmap(self, value, height=70, show_text=True, barcode_type="CODE128"):
        value = str(value or "SKU001")
        try:
            import barcode
            from barcode.writer import ImageWriter
            type_name = str(barcode_type or "CODE128").lower()
            if type_name not in {"code128", "code39", "ean13"}:
                type_name = "code128"
            kind = barcode.get(type_name, value, writer=ImageWriter())
            with tempfile.TemporaryDirectory() as folder:
                path = kind.save(os.path.join(folder, "barcode"), options={
                    "module_height": max(8.0, float(height) / 10),
                    "module_width": 0.25, "write_text": bool(show_text),
                    "quiet_zone": 2.0, "font_size": 10, "text_distance": 2.0,
                })
                pix = QPixmap(path)
                if not pix.isNull():
                    return pix
        except Exception:
            pass
        # Dependency-free fallback preview: deterministic CODE128-like bars.
        width = max(220, len(value) * 16 + 40)
        image = QImage(width, int(height) + (24 if show_text else 0),
                       QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        painter.setPen(Qt.PenStyle.NoPen)
        x = 10
        seed = sum(ord(ch) for ch in value) or 1
        while x < width - 10:
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            bar_w = 1 + (seed % 4)
            gap = 1 + ((seed >> 4) % 3)
            painter.fillRect(x, 0, bar_w, int(height), Qt.GlobalColor.black)
            x += bar_w + gap
        if show_text:
            painter.setPen(QColor("#111111"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(QRectF(0, height, width, 22),
                             Qt.AlignmentFlag.AlignCenter, value)
        painter.end()
        return QPixmap.fromImage(image)

    def add_barcode(self):
        return self.add_barcode_direct("SKU001", height=70, show_text=True)

    def add_barcode_direct(self, value, barcode_type="CODE128", height=70,
                           scale=1.0, show_text=True):
        pix = self._barcode_pixmap(value, height, show_text, barcode_type)
        item = QGraphicsPixmapItem(pix)
        item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        item.setScale(max(0.1, float(scale)))
        return self._add_item(item, "barcode", 20, 70)

    def add_qr(self):
        return self.add_qr_direct("SKU001")

    def add_qr_direct(self, value):
        pix = None
        try:
            import qrcode
            with tempfile.TemporaryDirectory() as folder:
                path = os.path.join(folder, "qr.png")
                qrcode.make(str(value)).save(path)
                pix = QPixmap(path)
        except Exception:
            pix = None
        if pix is None or pix.isNull():
            # Simple fallback QR-like image preview.
            image = QImage(180, 180, QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.white)
            painter = QPainter(image)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(Qt.GlobalColor.black)
            cell = 10
            for row in range(18):
                for col in range(18):
                    if ((row * 7 + col * 11 + len(str(value))) % 5) < 2:
                        painter.drawRect(col * cell, row * cell, cell, cell)
            painter.end()
            pix = QPixmap.fromImage(image)
        item = QGraphicsPixmapItem(pix)
        return self._add_item(item, "qr", 180, 60)

    def add_shape(self):
        item = QGraphicsRectItem(0, 0, 100, 55)
        item.setBrush(QBrush(QColor("#dbeafe")))
        item.setPen(QPen(QColor("#2563eb"), 2))
        return self._add_item(item, "shape", 70, 65)

    def add_image(self, path):
        pix = QPixmap(path)
        if pix.isNull():
            raise ValueError("The selected image could not be loaded.")
        return self._add_item(QGraphicsPixmapItem(pix), "image", 20, 20)

    def get_selected_item(self):
        for item in self.scene.selectedItems():
            if item is not self.label_rect and item.parentItem() is None:
                return item
        return None

    def set_position(self, x, y):
        item = self.get_selected_item()
        if item:
            item.setPos(float(x), float(y))
            self.viewport().update()

    def get_position(self):
        item = self.get_selected_item()
        if item:
            p = item.pos()
            return p.x(), p.y()
        return None, None

    def clear_canvas(self):
        self.scene.clear()
        self.label_rect = None
        self._create_label(400, 200)

    def set_label_size(self, w, h):
        if self.label_rect is None or self.label_rect.scene() is not self.scene:
            self._create_label(w, h)
        else:
            self.label_rect.setRect(QRectF(0, 0, max(1.0, float(w)), max(1.0, float(h))))
        self._set_scene_bounds()

    def resize_item(self, item, width, height):
        width, height = max(1.0, float(width)), max(1.0, float(height))
        if isinstance(item, QGraphicsRectItem):
            rect = item.rect()
            item.setRect(rect.x(), rect.y(), width, height)
        elif isinstance(item, QGraphicsTextItem):
            item.setTextWidth(width)
        elif isinstance(item, QGraphicsPixmapItem):
            pix = item.pixmap()
            if pix.width() and pix.height():
                item.setTransformOriginPoint(0, 0)
                item.setTransform(QTransform.fromScale(width / pix.width(),
                                                       height / pix.height()))
        else:
            bounds = item.boundingRect()
            if bounds.width() and bounds.height():
                item.setTransformOriginPoint(0, 0)
                item.setTransform(QTransform.fromScale(width / bounds.width(),
                                                       height / bounds.height()))
        self.viewport().update()
