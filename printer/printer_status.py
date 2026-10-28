import win32print


class PrinterStatus:

    @staticmethod
    def get_status(printer_name):

        try:

            handle = win32print.OpenPrinter(printer_name)

            info = win32print.GetPrinter(handle, 2)

            win32print.ClosePrinter(handle)

            status = info["Status"]

            return {

                "status": status,

                "online": status == 0,

                "driver": info["pDriverName"],

                "port": info["pPortName"]

            }

        except Exception as e:

            return {

                "status": "Unknown",

                "online": False,

                "driver": "",

                "port": "",

                "error": str(e)

            }