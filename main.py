# main.py

from ui.main_window import run_app


def run_backend_test():
    """
    Optional: Backend test function (can be removed in production)
    """

    from labels.dynamic_label_engine import DynamicLabelEngine
    from templates.template_loader import load_template
    from printer.printer_manager import PrinterManager

    printer_manager = PrinterManager()

    print("Available Printers:")
    print(printer_manager.get_printers())

    print("Default Printer:")
    print(printer_manager.get_default())

    template = load_template("templates/electronics_label.json")

    engine = DynamicLabelEngine(
        width_mm=template["size"]["width_mm"],
        height_mm=template["size"]["height_mm"]
    )

    product = {
        "product_name": "Gaming Mouse",
        "brand": "Logitech",
        "mrp": "999",
        "sku": "LOGI001",  
        "order_id": "ORD1001"
    }

    label_cmd = engine.build_label(
        product,
        template["fields"],
        quantity=1
    )

    print("\nGenerated Label Command:\n")
    print(label_cmd)

    # Uncomment to actually print
    # printer_manager.print_label(label_cmd)


if __name__ == "__main__":

    # 🔹 Run UI (Main Application)
    run_app()

    # 🔹 Optional: Backend testing (comment UI above and enable below if needed)
    # run_backend_test()     