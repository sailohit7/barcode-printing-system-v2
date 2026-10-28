# validators/template_validator.py

from barcode.barcode_registry import BarcodeRegistry


class TemplateValidator:

    def __init__(self):

        self.barcode_registry = BarcodeRegistry()

    # --------------------------------
    # Validate entire template
    # --------------------------------
    def validate(self, template):

        errors = []

        size = template.get("size")
        fields = template.get("fields")

        if not size:
            errors.append("Template missing 'size' section")

        if not fields:
            errors.append("Template missing 'fields' section")

        width = size.get("width_mm")
        height = size.get("height_mm")

        if width <= 0 or height <= 0:
            errors.append("Invalid label size")

        positions = []

        for field in fields:

            field_type = field.get("type")
            x = field.get("x")
            y = field.get("y")

            if x is None or y is None:
                errors.append(f"Field missing position: {field}")

            if x > width * 8:
                errors.append(f"Field outside label width: {field}")

            if y > height * 8:
                errors.append(f"Field outside label height: {field}")

            if field_type == "barcode":

                barcode_type = field.get("barcode_type")

                if not self.barcode_registry.is_supported(barcode_type):

                    errors.append(
                        f"Unsupported barcode type: {barcode_type}"
                    )

            positions.append((x, y))

        if errors:
            raise ValueError("\n".join(errors))

        return True