# barcode/barcode_registry.py

class BarcodeRegistry:

    def __init__(self):

        self._registry = {
            "CODE128": {
                "description": "Code 128 (Default)",
                "default": True
            },
            "EAN13": {
                "description": "EAN-13 Retail Barcode",
                "default": False
            },
            "CODE39": {
                "description": "Code 39",
                "default": False
            },
            "QR": {
                "description": "QR Code",
                "default": False
            }
        }

    # -----------------------------
    # Get supported barcodes
    # -----------------------------
    def get_supported(self):

        return list(self._registry.keys())

    # -----------------------------
    # Get default barcode
    # -----------------------------
    def get_default(self):

        for name, info in self._registry.items():

            if info["default"]:
                return name

        return "CODE128"

    # -----------------------------
    # Check barcode type
    # -----------------------------
    def is_supported(self, barcode_type):

        return barcode_type in self._registry

    # -----------------------------
    # Get barcode info
    # -----------------------------
    def get_info(self, barcode_type):

        return self._registry.get(barcode_type)