# printer/printer_utils.py

import win32print


def list_printers():

    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL |
        win32print.PRINTER_ENUM_CONNECTIONS
    )

    result = []

    for printer in printers:
        result.append(printer[2])

    return result


def get_default_printer():

    return win32print.GetDefaultPrinter()