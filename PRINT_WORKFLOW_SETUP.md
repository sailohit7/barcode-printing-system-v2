# Product → Barcode → Print → SQL workflow

## Run
From the project root:
```powershell
python -m pip install -r requirements.txt
python main.py
```

## Use
1. Dashboard → Import Excel; import a workbook with headers such as NAME, SKU, PRICE, QTY.
2. Select one product row in the table.
3. Click Generate Label.
4. Field Mapping defaults SKU/code fields to Barcode and name/price/quantity fields to Text. Adjust mappings as needed.
5. Click Preview Label. The app generates barcode images and opens the print screen.
6. Choose a printer, enter copies, click Print Label and Save to SQL, and confirm the Windows print dialog.
7. After the print job is submitted, the app attempts to insert the product and print details into `PrintHistory`.

## SQL Server
- The connection is configured in `database/sql_manager.py`.
- Current default connection uses ODBC Driver 17, server `LOHIT\SQLEXPRESS`, database `barcode_system`, and Windows integrated authentication.
- Change those settings to match your own SQL Server instance.
- Use Dashboard → Test SQL Connection to verify connectivity.
- The existing `PrintHistory` table must have the columns expected by `SQLManager.save_print`: `ProductName`, `SKU`, `Price`, `Qty`, `PrinterName`, `Copies`, and `PrintedAt`.

## Printing notes
- Printing uses PySide6 Qt Print Support and opens the Windows print dialog. The actual available options depend on the installed printer driver.
- For barcode labels, configure the label stock/page size in the printer driver before printing. Always test with one copy first.
- SQL history is saved only after the print dialog accepts and the print painter submits the job. If SQL fails after printing, the app warns that the print job was sent but history could not be saved.
- This version saves print history; it does not automatically persist the entire imported Excel workbook into a separate Products table.

## Barcode customization
- On Field Mapping, choose CODE128, CODE39, or EAN13.
- Set barcode height, scale, and whether the human-readable value appears beneath it.
- Click Preview to generate the label.
- On the Print screen, choose **Customize Label** to open Label Designer. Select an element to edit its position, size, rotation, opacity, or text font, then click **Continue to Print**.
- EAN13 requires a numeric value of 12 digits (checksum added) or 13 digits. For alphanumeric SKUs, use CODE128 or CODE39.
