import pyodbc
from database.connection_settings import load_connection_settings


class SQLManager:
    """SQL Server access using the connection profile saved in the application."""

    def __init__(self, settings=None):
        self.conn = None
        self.cursor = None
        self.settings = settings or load_connection_settings()
        self.connect()

    @staticmethod
    def build_connection_string(settings):
        driver = settings.get("driver", "SQL Server")
        server = settings.get("server", "").strip()
        database = settings.get("database", "").strip()
        if not driver or not server or not database:
            raise ValueError("ODBC driver, server/instance, and database are required.")
        parts = [f"DRIVER={{{driver}}}", f"SERVER={server}", f"DATABASE={database}"]
        if settings.get("authentication", "Windows") == "SQL Server":
            username = settings.get("username", "").strip()
            password = settings.get("password", "")
            if not username or not password:
                raise ValueError("Enter both SQL Server username and password.")
            parts.extend([f"UID={{{username}}}", f"PWD={{{password}}}"])
        else:
            parts.append("Trusted_Connection=yes")
        if settings.get("trust_server_certificate", True):
            parts.append("TrustServerCertificate=yes")
        return ";".join(parts) + ";"

    def connect(self):
        connection_string = self.build_connection_string(self.settings)
        self.conn = pyodbc.connect(connection_string, timeout=5)
        self.cursor = self.conn.cursor()
        self.ensure_schema()

    def ensure_schema(self):
        self.cursor.execute("""
            IF OBJECT_ID(N'dbo.PrintHistory', N'U') IS NULL
            BEGIN
                CREATE TABLE dbo.PrintHistory (
                    ID INT IDENTITY(1,1) PRIMARY KEY,
                    ProductName NVARCHAR(255) NULL,
                    SKU NVARCHAR(255) NULL,
                    Price NVARCHAR(100) NULL,
                    Qty NVARCHAR(100) NULL,
                    PrinterName NVARCHAR(255) NULL,
                    Copies INT NOT NULL CONSTRAINT DF_PrintHistory_Copies DEFAULT 1,
                    PrintedAt DATETIME2 NOT NULL CONSTRAINT DF_PrintHistory_PrintedAt DEFAULT SYSDATETIME()
                );
            END;
            IF OBJECT_ID(N'dbo.PrintQueue', N'U') IS NULL
            BEGIN
                CREATE TABLE dbo.PrintQueue (
                    ID INT IDENTITY(1,1) PRIMARY KEY,
                    ProductName NVARCHAR(255) NULL,
                    SKU NVARCHAR(255) NULL,
                    Price NVARCHAR(100) NULL,
                    Qty NVARCHAR(100) NULL,
                    Status NVARCHAR(50) NOT NULL CONSTRAINT DF_PrintQueue_Status DEFAULT 'Pending'
                );
            END;
        """)
        self.conn.commit()

    def test(self):
        self.cursor.execute("SELECT @@SERVERNAME, DB_NAME(), GETDATE()")
        return self.cursor.fetchone()

    def save_queue(self, data):
        self.cursor.execute("INSERT INTO dbo.PrintQueue (ProductName, SKU, Price, Qty, Status) VALUES (?, ?, ?, ?, ?)",
            data.get("name", ""), data.get("sku", ""), data.get("price", ""), data.get("qty", ""), "Pending")
        self.conn.commit()

    def get_queue(self):
        self.cursor.execute("SELECT * FROM dbo.PrintQueue ORDER BY ID DESC")
        return self.cursor.fetchall()

    def delete_queue_item(self, queue_id):
        self.cursor.execute("DELETE FROM dbo.PrintQueue WHERE ID=?", queue_id)
        self.conn.commit()

    def save_print_history(self, data):
        self.cursor.execute("INSERT INTO dbo.PrintHistory (ProductName, SKU, Price, Qty, PrintedAt) VALUES (?, ?, ?, ?, GETDATE())",
            data.get("name", ""), data.get("sku", ""), data.get("price", ""), data.get("qty", ""))
        self.conn.commit()

    def save_print(self, data, printer_name, copies):
        self.cursor.execute("INSERT INTO dbo.PrintHistory (ProductName, SKU, Price, Qty, PrinterName, Copies, PrintedAt) VALUES (?, ?, ?, ?, ?, ?, GETDATE())",
            data.get("name", ""), data.get("sku", ""), data.get("price", ""), data.get("qty", ""), printer_name, copies)
        self.conn.commit()

    def get_print_history(self):
        self.cursor.execute("SELECT * FROM dbo.PrintHistory ORDER BY PrintedAt DESC")
        return self.cursor.fetchall()

    def get_history(self):
        return self.get_print_history()

    def clear_history(self):
        self.cursor.execute("DELETE FROM dbo.PrintHistory")
        self.conn.commit()

    def search_history(self, keyword):
        self.cursor.execute("SELECT * FROM dbo.PrintHistory WHERE ProductName LIKE ? OR SKU LIKE ? ORDER BY PrintedAt DESC", f"%{keyword}%", f"%{keyword}%")
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
