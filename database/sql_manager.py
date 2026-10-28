import pyodbc


class SQLManager:

    def __init__(self):

        self.conn = pyodbc.connect(
            r"DRIVER={SQL Server};"
            r"SERVER=.\SQLEXPRESS;"
            r"DATABASE=barcode_system;"
            r"Trusted_Connection=yes;"
        )

        self.cursor = self.conn.cursor()

    # =====================================
    # TEST CONNECTION
    # =====================================
    def test(self):

        self.cursor.execute("SELECT GETDATE()")
        return self.cursor.fetchone()

    # =====================================
    # SAVE TO PRINT QUEUE
    # =====================================
    def save_queue(self, data):

        self.cursor.execute(
            """
            INSERT INTO PrintQueue
            (
                ProductName,
                SKU,
                Price,
                Qty,
                Status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            data.get("name", ""),
            data.get("sku", ""),
            data.get("price", ""),
            data.get("qty", ""),
            "Pending"
        )

        self.conn.commit()

    # =====================================
    # LOAD QUEUE
    # =====================================
    def get_queue(self):

        self.cursor.execute(
            """
            SELECT *
            FROM PrintQueue
            ORDER BY ID DESC
            """
        )

        return self.cursor.fetchall()

    # =====================================
    # DELETE QUEUE ITEM
    # =====================================
    def delete_queue_item(self, queue_id):

        self.cursor.execute(
            "DELETE FROM PrintQueue WHERE ID=?",
            queue_id
        )

        self.conn.commit()

    # =====================================
    # SAVE PRINT HISTORY
    # =====================================
    def save_print_history(self, data):

        self.cursor.execute(
            """
            INSERT INTO PrintHistory
            (
                ProductName,
                SKU,
                Price,
                Qty,
                PrintedAt
            )
            VALUES (?, ?, ?, ?, GETDATE())
            """,
            data.get("name", ""),
            data.get("sku", ""),
            data.get("price", ""),
            data.get("qty", "")
        )

        self.conn.commit()

    # =====================================
    # THIS FIXES YOUR MAIN WINDOW
    # =====================================
    def save_print(self, data, printer_name, copies):

        self.cursor.execute(
            """
            INSERT INTO PrintHistory
            (
                ProductName,
                SKU,
                Price,
                Qty,
                PrinterName,
                Copies,
                PrintedAt
            )
            VALUES (?, ?, ?, ?, ?, ?, GETDATE())
            """,
            data.get("name", ""),
            data.get("sku", ""),
            data.get("price", ""),
            data.get("qty", ""),
            printer_name,
            copies
        )

        self.conn.commit()

    # =====================================
    # LOAD PRINT HISTORY
    # =====================================
    def get_print_history(self):

        self.cursor.execute(
            """
            SELECT *
            FROM PrintHistory
            ORDER BY PrintedAt DESC
            """
        )

        return self.cursor.fetchall()

    # =====================================
    # BACKWARD COMPATIBILITY
    # =====================================
    def get_history(self):

        return self.get_print_history()

    # =====================================
    # CLEAR HISTORY
    # =====================================
    def clear_history(self):

        self.cursor.execute(
            "DELETE FROM PrintHistory"
        )

        self.conn.commit()

    # =====================================
    # SEARCH HISTORY
    # =====================================
    def search_history(self, keyword):

        self.cursor.execute(
            """
            SELECT *
            FROM PrintHistory
            WHERE ProductName LIKE ?
               OR SKU LIKE ?
            ORDER BY PrintedAt DESC
            """,
            f"%{keyword}%",
            f"%{keyword}%"
        )

        return self.cursor.fetchall()

    # =====================================
    # CLOSE CONNECTION
    # =====================================
    def close(self):

        if self.conn:
            self.conn.close()