# labels/pplb_templates.py

from validators.barcode_validator import (
    validate_code128,
    validate_ean13,
    calculate_ean13_checksum
)

from labels.label_layouts import DEFAULT_LABEL


# -------------------------------
# Common header builder
# -------------------------------

def build_header(layout: dict) -> str:
    return f"""
SIZE {layout['width_mm']} mm,{layout['height_mm']} mm
GAP {layout['gap_mm']} mm,0
CLS
""".strip()


# -------------------------------
# Phase 1 (still works)
# -------------------------------

def simple_test_label(layout: dict = DEFAULT_LABEL):
    header = build_header(layout)
    txt = layout["text"]

    return f"""
{header}

TEXT {txt['x']},{txt['y']},"{txt['font']}",0,{txt['x_mul']},{txt['y_mul']},"PHASE 1 TEST"

PRINT 1
""".strip()


# -------------------------------
# Code-128 Barcode Label
# -------------------------------

def code128_label(barcode_data: str, text: str, qty: int = 1, layout: dict = DEFAULT_LABEL):
    validate_code128(barcode_data)

    header = build_header(layout)
    bc = layout["barcode"]
    txt = layout["text"]

    return f"""
{header}

BARCODE {bc['x']},{bc['y']},"128",{bc['height']},1,0,{bc['narrow']},{bc['wide']},"{barcode_data}"
TEXT {txt['x']},{txt['y']},"{txt['font']}",0,{txt['x_mul']},{txt['y_mul']},"{text}"

PRINT {qty}
""".strip()


# -------------------------------
# EAN-13 Barcode Label
# -------------------------------

def ean13_label(barcode_data: str, text: str, qty: int = 1, layout: dict = DEFAULT_LABEL):
    validate_ean13(barcode_data)

    full_code = barcode_data + calculate_ean13_checksum(barcode_data)

    header = build_header(layout)
    bc = layout["barcode"]
    txt = layout["text"]

    return f"""
{header}

BARCODE {bc['x']},{bc['y']},"EAN13",{bc['height']},1,0,{bc['narrow']},{bc['wide']},"{full_code}"
TEXT {txt['x']},{txt['y']},"{txt['font']}",0,{txt['x_mul']},{txt['y_mul']},"{text}"

PRINT {qty}
""".strip()
