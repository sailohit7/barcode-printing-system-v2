import win32print


class PrinterManager:

    def __init__(self):
        pass

    def get_printers(self):
        """
        Returns complete printer information.
        """

        printers = []

        try:

            default = win32print.GetDefaultPrinter()

            for p in win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL |
                win32print.PRINTER_ENUM_CONNECTIONS
            ):

                name = p[2]

                try:

                    handle = win32print.OpenPrinter(name)

                    info = win32print.GetPrinter(handle, 2)

                    win32print.ClosePrinter(handle)

                    printers.append({

                        "name": name,

                        "driver": info["pDriverName"],

                        "port": info["pPortName"],

                        "default": name == default,

                        "status": "Online" if info["Status"] == 0 else "Busy"

                    })

                except Exception:

                    printers.append({

                        "name": name,

                        "driver": "",

                        "port": "",

                        "default": False,

                        "status": "Unknown"

                    })

        except Exception as e:

            print(e)

        return printers

    def get_default(self):
        return win32print.GetDefaultPrinter()

    def set_default(self, printer_name):
        try:
            win32print.SetDefaultPrinter(printer_name)
            return True
        except Exception:
            return False

    def print_test_page(self, printer_name):

        try:

            win32print.SetDefaultPrinter(printer_name)

            import os

            os.startfile(
                r"C:\Windows\System32\notepad.exe",
                "print"
            )

            return True

        except Exception as e:

            print(e)

            return False