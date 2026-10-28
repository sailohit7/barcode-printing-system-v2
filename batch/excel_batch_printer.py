# batch/excel_batch_printer.py

from openpyxl import load_workbook
from zipfile import BadZipFile

from labels.pplb_templates import code128_label, ean13_label
from printer.raw_printer import send_raw


# Required columns (normalized)
REQUIRED_COLUMNS = {
    "barcode_type",
    "barcode_data",
    "text",
    "quantity",
}


def normalize_header(header):
    """
    Normalize Excel headers safely.
    Returns None for empty cells.
    """
    if header is None:
        return None
    return str(header).strip().lower().replace(" ", "_")


def print_from_excel(xlsx_file_path: str, sheet_name: str = "Sheet1"):
    """
    Reads an Excel file (.xlsx) and prints labels in batch.
    - Auto-detects header row
    - Ignores empty columns
    - Handles Excel numeric corruption safely
    """

    # ---------- Load workbook ----------
    try:
        wb = load_workbook(xlsx_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {xlsx_file_path}")
    except BadZipFile:
        raise ValueError(
            "Invalid Excel file. Please save as 'Excel Workbook (*.xlsx)'"
        )

    if sheet_name not in wb.sheetnames:
        raise ValueError(
            f"Sheet '{sheet_name}' not found. Available: {wb.sheetnames}"
        )

    sheet = wb[sheet_name]

    # ---------- Auto-detect header row ----------
    raw_headers = None
    header_row_index = None

    for row in sheet.iter_rows(min_row=1, max_row=20):
        values = [cell.value for cell in row]
        if any(values):
            raw_headers = values
            header_row_index = row[0].row
            break

    if raw_headers is None:
        raise ValueError("No header row found in Excel file")

    # ---------- Normalize headers ----------
    headers = []
    header_indexes = []

    for idx, h in enumerate(raw_headers):
        nh = normalize_header(h)
        if nh:
            headers.append(nh)
            header_indexes.append(idx)

    missing = REQUIRED_COLUMNS - set(headers)
    if missing:
        raise ValueError(
            f"Missing required columns in Excel: {missing}\n"
            f"Found columns: {headers}"
        )

    # ---------- Process data rows ----------
    for row_num, row in enumerate(
        sheet.iter_rows(min_row=header_row_index + 1, values_only=True),
        start=1
    ):
        if not any(row):
            continue  # skip empty rows

        row_data = {}

        for h, col_idx in zip(headers, header_indexes):
            row_data[h] = row[col_idx]

        try:
            barcode_type = str(row_data["barcode_type"]).strip().upper()

            # Excel-safe barcode handling
            barcode_data = str(row_data["barcode_data"]).strip()
            if barcode_data.endswith(".0"):
                barcode_data = barcode_data[:-2]

            text = str(row_data["text"]).strip()
            qty = int(row_data["quantity"])

        except Exception as e:
            raise ValueError(
                f"Invalid data at Excel row {row_num}: {row_data}"
            ) from e

        print(f"\n[EXCEL] Processing row {row_num}: {barcode_type} | {barcode_data}")

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
            raise ValueError(
                f"Unsupported barcode type '{barcode_type}' at row {row_num}"
            )

        send_raw(cmd)
