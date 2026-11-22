import sqlite3
import pandas as pd


def get_total_farmers():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT COUNT(*) AS total_farmers FROM farmers", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def get_procurement_status_scheduled():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT COUNT(*) AS scheduled_count FROM procurements WHERE Status = 'Scheduled'", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def get_procurement_status_delayed():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT COUNT(*) AS delayed_count FROM procurements WHERE Status = 'Delayed'", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def get_procurement_status_completed():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT COUNT(*) AS completed_count FROM procurements WHERE Status = 'Completed'", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def get_procurement_status_cancelled():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT COUNT(*) AS cancelled_count FROM procurements WHERE Status = 'Cancelled'", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def get_crop_summary():
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT Crop, COUNT(*) AS procurement_count FROM procurements GROUP BY Crop", conn)
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


def get_daily_report(date):
    conn = sqlite3.connect("database.db")

    try:
        data = pd.read_sql_query("SELECT * FROM procurements WHERE Procurement_date = ?", conn, params=(date,))
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()
