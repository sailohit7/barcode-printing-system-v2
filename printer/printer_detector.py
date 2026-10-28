import win32print


class PrinterDetector:

    @staticmethod
    def get_printers():
        """
        Returns a list of installed printers.
        """

        printers = []

        try:
            flags = (
                win32print.PRINTER_ENUM_LOCAL |
                win32print.PRINTER_ENUM_CONNECTIONS
            )

            printer_list = win32print.EnumPrinters(flags)

            default_printer = ""

            try:
                default_printer = win32print.GetDefaultPrinter()
            except Exception:
                pass

            for printer in printer_list:

                name = printer[2]

                printers.append({
                    "name": name,
                    "default": name == default_printer
                })

        except Exception as e:

            print("Printer Detection Error:", e)

        return printers