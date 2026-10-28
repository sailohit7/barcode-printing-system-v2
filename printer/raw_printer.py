# printer/raw_printer.py

import win32print


def send_raw(data, printer_name=None):
    """
    Send RAW printer commands directly to Windows printer spooler
    """

    # If printer not provided, use default printer
    if printer_name is None:
        printer_name = win32print.GetDefaultPrinter()

    try:

        printer = win32print.OpenPrinter(printer_name)

        job = win32print.StartDocPrinter(
            printer,
            1,
            ("RawLabelJob", None, "RAW")
        )

        win32print.StartPagePrinter(printer)

        win32print.WritePrinter(printer, data.encode("utf-8"))

        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)

        win32print.ClosePrinter(printer)

        print(f"[PRINTED] Sent to printer: {printer_name}")

    except Exception as e:

        print("[PRINT ERROR]", e)