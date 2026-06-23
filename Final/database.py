import sqlite3

class Database:
    def __init__(self):
        self.database_name = "database"
        self.conn = None
        self.cur = None
        self.cols_list = []

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)
        self.cur = self.conn.cursor()
        print("Database Connected.")

    def close(self):
        self.conn.close()
        print("Database Closed.")

    def commit(self):
        self.conn.commit()

    def get_opcode_from_db(self):
        self.cur.execute(f"SELECT opcode FROM commands")
        rows = self.cur.fetchall()
        self.cols_list = [row[0] for row in rows]


# Query function: Implement get_action_for_opcode(opcode: str) -> str | None:
# Use parameterized queries (? placeholders).
# Return the action string or None if not found.
# Handle database errors cleanly.


    def get_action_for_opcode(self, opcode: str) -> str:
        if self.conn:
            self.cur.execute(f"SELECT response FROM commands where opcode = ?", (opcode,))
            row = self.cur.fetchone()
            result = row[0] if row else "Not Found"
            return result
        return "Not connected to Database"
