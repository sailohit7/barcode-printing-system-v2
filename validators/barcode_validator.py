# validators/barcode_validator.py

def validate_ascii(data: str):
    if not data:
        raise ValueError("Barcode data cannot be empty")

    if not data.isascii():
        raise ValueError("Barcode data must contain ASCII characters only")


def validate_code128(data: str):
    """
    Code-128 rules:
    - ASCII allowed
    - Any length
    """
    validate_ascii(data)


def validate_ean13(data: str):
    """
    EAN-13 rules:
    - Exactly 12 numeric digits (checksum added automatically)
    """
    if not data.isdigit():
        raise ValueError("EAN-13 must contain digits only")

    if len(data) != 12:
        raise ValueError("EAN-13 requires exactly 12 digits")


def calculate_ean13_checksum(data: str) -> str:
    """
    Calculates the 13th digit (checksum) for EAN-13
    """
    total = 0
    for i, digit in enumerate(data):
        n = int(digit)
        total += n * 3 if i % 2 else n

    checksum = (10 - (total % 10)) % 10
    return str(checksum)
