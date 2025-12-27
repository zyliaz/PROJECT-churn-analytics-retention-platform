"""
Day 1 - Data Exploration Script
================================
This script performs initial data exploration for users, subscriptions, and events tables.
It validates schema understanding, checks data quality, and documents basic observations.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path

# Configuration
DB_CONFIG = {
    'host': 'mysql-tcs.drillinsight.com',
    'database': 'churn_analytics',
    'user': 'yuejia_zhang',  # Update with your MySQL username
    'password': 'Test123!'   # Update with your MySQL password
}

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'raw'
EVENTS_FILE = DATA_DIR / 'user_events.csv'

def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✓ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        print("Note: Make sure MySQL is running and credentials are correct")
        return None

def explore_users_table(connection):
    """Explore users table"""
    print("\n" + "="*60)
    print("USERS TABLE EXPLORATION")
    print("="*60)
    
    query = """
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(*) - COUNT(DISTINCT user_id) as duplicate_user_ids,
        COUNT(gender) as gender_count,
        COUNT(senior_citizen) as senior_citizen_count,
        COUNT(has_partner) as has_partner_count,
        COUNT(has_dependents) as has_dependents_count
    FROM users
    """
    
    df = pd.read_sql(query, connection)
    print(f"\nTotal rows: {df['total_rows'].iloc[0]:,}")
    print(f"Unique users: {df['unique_users'].iloc[0]:,}")
    print(f"Duplicate user_ids: {df['duplicate_user_ids'].iloc[0]:,}")
    
    # Check data types and nulls
    query_schema = """
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        IS_NULLABLE,
        COLUMN_DEFAULT
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'churn_analytics' 
    AND TABLE_NAME = 'users'
    ORDER BY ORDINAL_POSITION
    """
    schema_df = pd.read_sql(query_schema, connection)
    print("\nColumn Information:")
    print(schema_df.to_string(index=False))
    
    # Gender distribution
    query_gender = "SELECT gender, COUNT(*) as count FROM users GROUP BY gender"
    gender_df = pd.read_sql(query_gender, connection)
    print("\nGender Distribution:")
    print(gender_df.to_string(index=False))
    
    return df

def explore_subscriptions_table(connection):
    """Explore subscriptions table"""
    print("\n" + "="*60)
    print("SUBSCRIPTIONS TABLE EXPLORATION")
    print("="*60)
    
    query = """
    SELECT 
        COUNT(*) as total_rows,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(*) - COUNT(DISTINCT user_id) as duplicate_user_ids,
        COUNT(signup_date) as signup_date_count,
        COUNT(cancel_date) as cancel_date_count,
        COUNT(status) as status_count,
        COUNT(plan) as plan_count
    FROM subscriptions
    """
    
    df = pd.read_sql(query, connection)
    print(f"\nTotal rows: {df['total_rows'].iloc[0]:,}")
    print(f"Unique users: {df['unique_users'].iloc[0]:,}")
    print(f"Duplicate user_ids: {df['duplicate_user_ids'].iloc[0]:,}")
    
    # Check data types
    query_schema = """
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        IS_NULLABLE,
        COLUMN_DEFAULT
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'churn_analytics' 
    AND TABLE_NAME = 'subscriptions'
    ORDER BY ORDINAL_POSITION
    """
    schema_df = pd.read_sql(query_schema, connection)
    print("\nColumn Information:")
    print(schema_df.to_string(index=False))
    
    # Status distribution
    query_status = "SELECT status, COUNT(*) as count FROM subscriptions GROUP BY status"
    status_df = pd.read_sql(query_status, connection)
    print("\nStatus Distribution:")
    print(status_df.to_string(index=False))
    
    # Plan distribution
    query_plan = "SELECT plan, COUNT(*) as count FROM subscriptions GROUP BY plan ORDER BY count DESC"
    plan_df = pd.read_sql(query_plan, connection)
    print("\nPlan Distribution:")
    print(plan_df.to_string(index=False))
    
    # Date ranges
    query_dates = """
    SELECT 
        MIN(signup_date) as earliest_signup,
        MAX(signup_date) as latest_signup,
        MIN(cancel_date) as earliest_cancel,
        MAX(cancel_date) as latest_cancel
    FROM subscriptions
    """
    dates_df = pd.read_sql(query_dates, connection)
    print("\nDate Ranges:")
    print(f"Earliest signup: {dates_df['earliest_signup'].iloc[0]}")
    print(f"Latest signup: {dates_df['latest_signup'].iloc[0]}")
    print(f"Earliest cancel: {dates_df['earliest_cancel'].iloc[0]}")
    print(f"Latest cancel: {dates_df['latest_cancel'].iloc[0]}")
    
    return df

def validate_foreign_keys(connection):
    """Validate foreign key relationships"""
    print("\n" + "="*60)
    print("FOREIGN KEY VALIDATION")
    print("="*60)
    
    # Check: Every user_id in subscriptions should appear in users
    query_sub_to_users = """
    SELECT COUNT(*) as orphaned_subscriptions
    FROM subscriptions s
    LEFT JOIN users u ON s.user_id = u.user_id
    WHERE u.user_id IS NULL
    """
    result = pd.read_sql(query_sub_to_users, connection)
    orphaned_subs = result['orphaned_subscriptions'].iloc[0]
    print(f"\nOrphaned subscriptions (user_id not in users): {orphaned_subs}")
    
    # Check: Users without subscriptions (fake users)
    query_users_without_subs = """
    SELECT COUNT(*) as users_without_subscriptions
    FROM users u
    LEFT JOIN subscriptions s ON u.user_id = s.user_id
    WHERE s.user_id IS NULL
    """
    result = pd.read_sql(query_users_without_subs, connection)
    users_no_subs = result['users_without_subscriptions'].iloc[0]
    print(f"Users without subscriptions (fake users): {users_no_subs:,}")
    
    # Check: Users with subscriptions
    query_users_with_subs = """
    SELECT COUNT(DISTINCT u.user_id) as users_with_subscriptions
    FROM users u
    INNER JOIN subscriptions s ON u.user_id = s.user_id
    """
    result = pd.read_sql(query_users_with_subs, connection)
    users_with_subs = result['users_with_subscriptions'].iloc[0]
    print(f"Users with subscriptions: {users_with_subs:,}")
    
    return orphaned_subs == 0

def explore_events_file():
    """Explore user_events.csv file"""
    print("\n" + "="*60)
    print("USER EVENTS FILE EXPLORATION")
    print("="*60)
    
    if not EVENTS_FILE.exists():
        print(f"✗ Events file not found at: {EVENTS_FILE}")
        return None
    
    print(f"\nReading events file: {EVENTS_FILE}")
    print("Note: This may take a while for large files...")
    
    # Read in chunks to handle large files
    chunk_size = 100000
    total_rows = 0
    columns = None
    event_types = {}
    device_types = {}
    unique_users = set()
    
    try:
        for chunk in pd.read_csv(EVENTS_FILE, chunksize=chunk_size):
            total_rows += len(chunk)
            if columns is None:
                columns = chunk.columns.tolist()
            
            # Count event types
            for event_type in chunk['event_type'].value_counts().to_dict():
                event_types[event_type] = event_types.get(event_type, 0) + chunk['event_type'].value_counts()[event_type]
            
            # Count device types
            for device_type in chunk['device_type'].value_counts().to_dict():
                device_types[device_type] = device_types.get(device_type, 0) + chunk['device_type'].value_counts()[device_type]
            
            # Collect unique users
            unique_users.update(chunk['user_id'].unique())
        
        print(f"\nTotal rows: {total_rows:,}")
        print(f"Total columns: {len(columns)}")
        print(f"Columns: {', '.join(columns)}")
        print(f"Unique users: {len(unique_users):,}")
        
        # Check for nulls (sample from first chunk)
        first_chunk = pd.read_csv(EVENTS_FILE, nrows=chunk_size)
        print("\nNull counts (sample):")
        null_counts = first_chunk.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                print(f"  {col}: {count:,} nulls")
        
        # Event type distribution
        print("\nEvent Type Distribution:")
        for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_rows) * 100
            print(f"  {event_type}: {count:,} ({pct:.2f}%)")
        
        # Device type distribution
        print("\nDevice Type Distribution:")
        for device_type, count in sorted(device_types.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_rows) * 100
            print(f"  {device_type}: {count:,} ({pct:.2f}%)")
        
        # Date range (sample)
        first_chunk['event_time'] = pd.to_datetime(first_chunk['event_time'])
        print(f"\nDate Range (sample):")
        print(f"  Earliest event: {first_chunk['event_time'].min()}")
        print(f"  Latest event: {first_chunk['event_time'].max()}")
        
        return {
            'total_rows': total_rows,
            'columns': columns,
            'unique_users': len(unique_users),
            'event_types': event_types,
            'device_types': device_types
        }
        
    except Exception as e:
        print(f"✗ Error reading events file: {e}")
        return None

def main():
    """Main execution function"""
    print("="*60)
    print("DAY 1: DATA EXPLORATION")
    print("="*60)
    
    # Connect to MySQL
    connection = connect_to_mysql()
    
    if connection:
        try:
            # Explore users table
            users_info = explore_users_table(connection)
            
            # Explore subscriptions table
            subscriptions_info = explore_subscriptions_table(connection)
            
            # Validate foreign keys
            fk_valid = validate_foreign_keys(connection)
            
            if not fk_valid:
                print("\n⚠ WARNING: Foreign key validation failed!")
            
        finally:
            connection.close()
            print("\n✓ MySQL connection closed")
    else:
        print("\n⚠ Skipping MySQL table exploration (connection failed)")
        print("  Make sure MySQL is running and update DB_CONFIG in the script")
    
    # Explore events file
    events_info = explore_events_file()
    
    print("\n" + "="*60)
    print("EXPLORATION COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the output above")
    print("2. Document any issues found")
    print("3. Proceed to Day 2: Basic KPI Validation")

if __name__ == "__main__":
    main()