# labels/dynamic_label_engine.py

from validators.barcode_validator import (
    validate_code128,
    validate_ean13,
    calculate_ean13_checksum
)

from barcode.barcode_registry import BarcodeRegistry


class DynamicLabelEngine:

    def __init__(self, width_mm=100, height_mm=50, gap_mm=2):

        self.width_mm = width_mm
        self.height_mm = height_mm
        self.gap_mm = gap_mm

        self.line_spacing = 20
        self.commands = []

        # Initialize barcode registry
        self.barcode_registry = BarcodeRegistry()

    # ---------------------------------------------------------
    # Add Label Header
    # ---------------------------------------------------------
    def _add_header(self):

        header = f"""
SIZE {self.width_mm} mm,{self.height_mm} mm
GAP {self.gap_mm} mm,0
CLS
""".strip()

        self.commands.append(header)

    # ---------------------------------------------------------
    # Text wrapping
    # ---------------------------------------------------------
    def _wrap_text(self, text, max_chars=25):

        words = text.split()

        lines = []
        current_line = ""

        for word in words:

            if len(current_line + word) < max_chars:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

    # ---------------------------------------------------------
    # Add text at position
    # ---------------------------------------------------------
    def _add_text_at_position(self, text, x, y, font="0", x_mul=10, y_mul=10):

        lines = self._wrap_text(text)

        for i, line in enumerate(lines):

            y_pos = y + (i * self.line_spacing)

            cmd = f'TEXT {x},{y_pos},"{font}",0,{x_mul},{y_mul},"{line}"'

            self.commands.append(cmd)

    # ---------------------------------------------------------
    # Add barcode at position
    # ---------------------------------------------------------
    def _add_barcode_at_position(self, data, barcode_type, x, y, height=80):

        # Check barcode registry
        if not self.barcode_registry.is_supported(barcode_type):

            raise ValueError(f"Unsupported barcode type: {barcode_type}")

        # Generate barcode command
        if barcode_type == "CODE128":

            validate_code128(data)

            cmd = f'BARCODE {x},{y},"128",{height},1,0,2,2,"{data}"'

        elif barcode_type == "EAN13":

            validate_ean13(data)

            full_code = data + calculate_ean13_checksum(data)

            cmd = f'BARCODE {x},{y},"EAN13",{height},1,0,2,2,"{full_code}"'

        elif barcode_type == "CODE39":

            cmd = f'BARCODE {x},{y},"39",{height},1,0,2,2,"{data}"'

        elif barcode_type == "QR":

            cmd = f'QRCODE {x},{y},L,5,A,0,"{data}"'

        else:

            raise ValueError(f"Unsupported barcode type: {barcode_type}")

        self.commands.append(cmd)

    # ---------------------------------------------------------
    # Build label
    # ---------------------------------------------------------
    def build_label(self, product_data: dict, field_config: list, quantity: int = 1):

        self.commands = []

        self._add_header()

        for field in field_config:

            field_type = field["type"]
            key = field["key"]

            if key not in product_data:
                continue

            value = str(product_data[key])

            x = field.get("x", 20)
            y = field.get("y", 20)

            if field_type == "text":

                label = field.get("label")

                if label:
                    value = f"{label}: {value}"

                self._add_text_at_position(value, x, y)

            elif field_type == "barcode":

                barcode_type = field.get(
                    "barcode_type",
                    self.barcode_registry.get_default()
                )

                self._add_barcode_at_position(value, barcode_type, x, y)

        self.commands.append(f"PRINT {quantity}")

        return "\n".join(self.commands)