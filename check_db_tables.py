#!/usr/bin/env python3
import sqlite3

try:
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("الجداول الموجودة:")
    for table in tables:
        print(f"  - {table}")
    
    conn.close()
    
except Exception as e:
    print(f"خطأ: {e}")
