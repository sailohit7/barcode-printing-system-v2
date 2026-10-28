# batch/csv_batch_printer.py

import csv
from labels.pplb_templates import code128_label, ean13_label
from printer.raw_printer import send_raw


def print_from_csv(csv_file_path: str):
    """
    Reads a CSV file and prints labels in batch.
    """

    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row_num, row in enumerate(reader, start=1):
            barcode_type = row["barcode_type"].strip().upper()
            barcode_data = row["barcode_data"].strip()
            text = row["text"].strip()
            qty = int(row["quantity"])

            print(f"\n[CSV] Processing row {row_num}: {barcode_type} | {barcode_data}")

            if barcode_type == "CODE128":
                cmd = code128_label(
                    barcode_data=barcode_data,
                    text=text,
                    qty=qty
                )

            elif barcode_type == "EAN13":
                cmd = ean13_label(
                    barcode_data=barcode_data,
                    text=text,
                    qty=qty
                )

            else:
                raise ValueError(f"Unsupported barcode type: {barcode_type}")

            send_raw(cmd)
