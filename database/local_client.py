import sqlite3
import json
import os
from pathlib import Path

DB_FILE = Path(__file__).parent / "local_attendance.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number TEXT UNIQUE NOT NULL,
        admission_number TEXT,
        student_name TEXT NOT NULL,
        class TEXT NOT NULL,
        section TEXT NOT NULL,
        gender TEXT,
        dob TEXT,
        parent_name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        photo1 TEXT,
        photo2 TEXT,
        photo3 TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS face_encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        photo_number INTEGER NOT NULL,
        encoding TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        attendance_date TEXT NOT NULL,
        attendance_time TEXT NOT NULL,
        status TEXT NOT NULL,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

init_db()

class QueryResponse:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"QueryResponse(data={self.data})"

class TableQuery:
    def __init__(self, table_name):
        self.table_name = table_name
        self.action = "select"  # "select", "insert", "delete"
        self.select_columns = "*"
        self.insert_data = None
        self.filters = []  # list of (column, value)
        self.order_by = [] # list of (column, desc_bool)
        self.is_single = False

    def insert(self, data):
        self.action = "insert"
        self.insert_data = data
        return self

    def select(self, columns="*"):
        self.action = "select"
        self.select_columns = columns
        return self

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def order(self, column, desc=False):
        self.order_by.append((column, desc))
        return self

    def single(self):
        self.is_single = True
        return self

    def delete(self):
        self.action = "delete"
        return self

    def execute(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        try:
            if self.action == "insert":
                if isinstance(self.insert_data, dict):
                    rows = [self.insert_data]
                else:
                    rows = self.insert_data

                inserted_rows = []
                for row_data in rows:
                    cols = list(row_data.keys())
                    vals = []
                    for k in cols:
                        v = row_data[k]
                        if isinstance(v, (list, dict)):
                            vals.append(json.dumps(v))
                        else:
                            vals.append(v)

                    placeholders = ", ".join(["?"] * len(cols))
                    sql = f"INSERT INTO {self.table_name} ({', '.join(cols)}) VALUES ({placeholders})"
                    c.execute(sql, vals)
                    row_id = c.lastrowid
                    
                    # fetch inserted row
                    c.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (row_id,))
                    inserted = dict(c.fetchone())
                    if "encoding" in inserted and isinstance(inserted["encoding"], str):
                        try:
                            inserted["encoding"] = json.loads(inserted["encoding"])
                        except Exception:
                            pass
                    inserted_rows.append(inserted)

                conn.commit()
                return QueryResponse(inserted_rows)

            elif self.action == "delete":
                where_clauses = []
                where_vals = []
                for col, val in self.filters:
                    where_clauses.append(f"{col} = ?")
                    where_vals.append(val)
                where_sql = f" WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
                sql = f"DELETE FROM {self.table_name}{where_sql}"
                c.execute(sql, where_vals)
                conn.commit()
                return QueryResponse([])

            elif self.action == "select":
                # Check if this is a join on attendance_records with students
                if self.table_name == "attendance_records" and "students(" in self.select_columns:
                    sql = """
                    SELECT a.id, a.student_id, a.attendance_date, a.attendance_time, a.status, a.confidence,
                           s.student_name, s.roll_number, s.class, s.section
                    FROM attendance_records a
                    LEFT JOIN students s ON a.student_id = s.id
                    """
                    where_clauses = []
                    where_vals = []
                    for col, val in self.filters:
                        where_clauses.append(f"a.{col} = ?")
                        where_vals.append(val)
                    if where_clauses:
                        sql += f" WHERE {' AND '.join(where_clauses)}"
                    if self.order_by:
                        orders = []
                        for col, desc in self.order_by:
                            orders.append(f"a.{col} {'DESC' if desc else 'ASC'}")
                        sql += f" ORDER BY {', '.join(orders)}"

                    c.execute(sql, where_vals)
                    results = []
                    for row in c.fetchall():
                        r = dict(row)
                        item = {
                            "attendance_date": r["attendance_date"],
                            "attendance_time": r["attendance_time"],
                            "status": r["status"],
                            "confidence": r["confidence"],
                            "students": {
                                "student_name": r["student_name"],
                                "roll_number": r["roll_number"],
                                "class": r["class"],
                                "section": r["section"],
                            }
                        }
                        results.append(item)

                    if self.is_single:
                        return QueryResponse(results[0] if results else None)
                    return QueryResponse(results)

                # Standard SELECT
                sql = f"SELECT * FROM {self.table_name}"
                where_clauses = []
                where_vals = []
                for col, val in self.filters:
                    where_clauses.append(f"{col} = ?")
                    where_vals.append(val)
                if where_clauses:
                    sql += f" WHERE {' AND '.join(where_clauses)}"
                if self.order_by:
                    orders = []
                    for col, desc in self.order_by:
                        orders.append(f"{col} {'DESC' if desc else 'ASC'}")
                    sql += f" ORDER BY {', '.join(orders)}"

                c.execute(sql, where_vals)
                rows = [dict(row) for row in c.fetchall()]
                for r in rows:
                    if "encoding" in r and isinstance(r["encoding"], str):
                        try:
                            r["encoding"] = json.loads(r["encoding"])
                        except Exception:
                            pass

                if self.is_single:
                    return QueryResponse(rows[0] if rows else None)
                return QueryResponse(rows)

        finally:
            conn.close()

class LocalSupabaseClient:
    def table(self, table_name):
        return TableQuery(table_name)

