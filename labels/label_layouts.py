# labels/label_layouts.py

"""
Label layout definitions.
This file controls HOW the label looks.
"""

DEFAULT_LABEL = {
    "width_mm": 60,
    "height_mm": 40,
    "gap_mm": 2,

    "barcode": {
        "x": 50,
        "y": 50,
        "height": 100,
        "narrow": 2,
        "wide": 2
    },

    "text": {
        "x": 50,
        "y": 170,
        "font": "0",
        "x_mul": 12,
        "y_mul": 12
    }
}
