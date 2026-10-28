# labels/label_configs.py

ELECTRONICS_LABEL = {
    "size": {
        "width_mm": 100,
        "height_mm": 60
    },

    "fields": [
        {"type": "text", "key": "product_name", "label": "Product"},
        {"type": "text", "key": "brand", "label": "Brand"},
        {"type": "text", "key": "mrp", "label": "MRP"},

        {"type": "barcode", "key": "sku", "barcode_type": "CODE128"}
    ]
}


PHARMA_LABEL = {
    "size": {
        "width_mm": 80,
        "height_mm": 50
    },

    "fields": [
        {"type": "text", "key": "product_name"},
        {"type": "text", "key": "batch", "label": "Batch"},
        {"type": "text", "key": "mfd", "label": "MFD"},
        {"type": "text", "key": "exp", "label": "EXP"},

        {"type": "barcode", "key": "sku", "barcode_type": "EAN13"}
    ]
}


DEFAULT_LABEL = {
    "size": {
        "width_mm": 90,
        "height_mm": 50
    },

    "fields": [
        {"type": "text", "key": "product_name"},
        {"type": "barcode", "key": "sku", "barcode_type": "CODE128"}
    ]
}