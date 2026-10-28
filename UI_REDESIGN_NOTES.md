# Barcode Printing System — UI Update

## What changed
- Refined dark enterprise theme with blue accents and rounded panels.
- Added dashboard metric cards for product rows, data fields, installed printers, and canvas elements.
- Added fade transitions and active navigation highlighting.
- Improved Excel/CSV import feedback and empty-data handling.
- Connected Save History to SQL Server with error feedback and cleanup.
- SQL History now loads when opened and has clearer status feedback.
- Printer Manager refresh and Printer Connection controls use the existing Windows PrinterManager backend.
- Print record handling validates copy count and clearly states that this workflow currently records the request in SQL Server; it does not yet render/send the designed label as a physical print job.

## Install
Run from the project root:
```powershell
python -m pip install -r requirements.txt
```
Then:
```powershell
python main.py
```

## Backend configuration notes
- SQL Server connection settings are in `database/sql_manager.py`; review server/database names for your machine before running.
- Printer enumeration and test-page requests use Windows printer services via `pywin32`.
- Test page output is a Windows/Notepad print request, not the application's designed label.
- SQL history requires the expected `PrintHistory` table schema to exist.
