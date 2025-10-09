#!/usr/bin/env python
"""
Script to check SQLite database contents before migration
"""
import sqlite3
import json
import os

def check_sqlite_database():
    """Check SQLite database structure and data"""
    db_path = 'db.sqlite3'
    
    if not os.path.exists(db_path):
        print("❌ SQLite database not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📊 SQLite Database Analysis:")
        print("=" * 50)
        print(f"Database file: {db_path}")
        print(f"Tables found: {len(tables)}")
        print()
        
        total_records = 0
        table_info = {}
        
        for table in tables:
            table_name = table[0]
            
            # Skip Django system tables
            if table_name.startswith('django_') or table_name.startswith('auth_'):
                continue
                
            # Get record count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            table_info[table_name] = {
                'count': count,
                'columns': [col[1] for col in columns]
            }
            
            print(f"📋 Table: {table_name}")
            print(f"   Records: {count}")
            print(f"   Columns: {', '.join([col[1] for col in columns])}")
            print()
        
        print(f"📈 Total user data records: {total_records}")
        
        # Check for specific important tables
        important_tables = ['fbc_users_customuser', 'fbc_books_book', 'fbc_books_ebook', 'fbc_payments_payment']
        print("\n🔍 Checking important tables:")
        for table in important_tables:
            if table in table_info:
                print(f"✅ {table}: {table_info[table]['count']} records")
            else:
                print(f"❌ {table}: Not found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")
        return False

if __name__ == '__main__':
    check_sqlite_database()
