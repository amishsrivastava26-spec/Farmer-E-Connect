
import sqlite3


# 1. Create Farmer Table
def farmer_table():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farmers (
                Farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Mobile INTEGER UNIQUE NOT NULL,
                Village TEXT NOT NULL,
                Village_pin INTEGER NOT NULL,
                Crop TEXT NOT NULL,
                Password_hash TEXT
            )
        """)

        conn.commit()
        print("Farmer table created successfully")

    except Exception as e:
        print(f"Error creating table: {e}")

    finally:
        conn.close()


# 2. Add Farmer Details
def add_farmer(Name, Mobile, Village, Village_pin, Crop, Password_hash=None):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO farmers (Name, Mobile, Village, Village_pin, Crop, Password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (Name, Mobile, Village, Village_pin, Crop, Password_hash))

        conn.commit()
        print("Farmer inserted successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error adding farmer details: {e}")
        return False

    finally:
        conn.close()


# 3. Get All Farmer Details
def get_all_details():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM farmers")

        details = cursor.fetchall()

        for detail in details:
            print(detail)

        print(f"Total farmers retrieved: {len(details)}")
        return details

    finally:
        conn.close()


# 4. Get Farmer Details By ID
def get_details_by_id(Farmer_Id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM farmers WHERE Farmer_id = ?",
            (Farmer_Id,)
        )

        details = cursor.fetchall()

        if details:
            for detail in details:
                print(detail)
        else:
            print(f"No farmer found with ID {Farmer_Id}")

        return details

    finally:
        conn.close()


# 5. Update Farmer Mobile Number
def update_farmer_mobile(Farmer_Id, new_mobile):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE farmers SET Mobile = ? WHERE Farmer_Id = ?",
            (new_mobile, Farmer_Id)
        )

        if cursor.rowcount == 0:
            print(f"No farmer found with ID {Farmer_Id}")
            return False

        conn.commit()

        print("Details updated successfully!")
        print("Updated details are:")

        cursor.execute(
            "SELECT * FROM farmers WHERE Farmer_Id = ?",
            (Farmer_Id,)
        )

        details = cursor.fetchone()
        print(details)

        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating farmer details: {e}")
        return False

    finally:
        conn.close()

def delete_record(Farmer_Id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM farmers WHERE Farmer_id = ?",
            (Farmer_Id,)
        )

        if cursor.rowcount == 0:
            print(f"No farmer found with ID {Farmer_Id}")
            return False

        conn.commit()
        print("Farmer record deleted successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error deleting farmer record: {e}")
        return False

    finally:
        conn.close()

        
def update_farmer_crop(Farmer_Id, new_crop):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE farmers SET Crop=? WHERE Farmer_Id=?",
            (new_crop, Farmer_Id)
        )

        conn.commit()
        print("Now details are:-")
        get_details_by_id(Farmer_Id)

        print("Crop updated successfully")

        
        return True

        

    except Exception as e:
        conn.rollback()
        print(f"Error updating farmer details: {e}")
        return False

    finally:
        conn.close()

def update_farmer_village(Farmer_Id, new_village):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE farmers SET Village=? WHERE Farmer_Id=?",
            (new_village, Farmer_Id)
        )

        conn.commit()
        print("Now details are:-")
        get_details_by_id(Farmer_Id)

        print("Village updated successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating farmer details: {e}")
        return False

    finally:
        conn.close()

def update_farmer_village_pin(Farmer_Id, new_village_pin):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE farmers SET Village_pin=? WHERE Farmer_Id=?",
            (new_village_pin, Farmer_Id)
        )

        conn.commit()
        print("Now details are:-")
        get_details_by_id(Farmer_Id)

        print("Village PIN updated successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating farmer details: {e}")
        return False

    finally:
        conn.close()



# Procurement Table

def procurement_table():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS procurements (
                Procurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Farmer_id INTEGER NOT NULL,
                Name TEXT NOT NULL,
                Procurement_token TEXT UNIQUE NOT NULL,
                Procurement_date TEXT NOT NULL,
                Quantity REAL NOT NULL,
                Crop TEXT NOT NULL,
                Status TEXT NOT NULL DEFAULT 'Scheduled',

                FOREIGN KEY (Farmer_id) REFERENCES farmers(Farmer_id)
            )
        """)

        conn.commit()
        print("Procurement table created successfully")

    except Exception as e:
        print(f"Error creating procurement table: {e}")

    finally:
        conn.close()


# Notification Table

def notification_table():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                Notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Farmer_id INTEGER NOT NULL,
                Name TEXT NOT NULL,
                Message TEXT NOT NULL,
                Sent_date TEXT NOT NULL,
                Status TEXT NOT NULL,

                FOREIGN KEY (Farmer_id) REFERENCES farmers(Farmer_id)
            )
        """)

        conn.commit()
        print("Notifications table created successfully")

    except Exception as e:
        print(f"Error creating notification table: {e}")

    finally:
        conn.close()


def help_request_table():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS help_requests (
                Help_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Farmer_id INTEGER NOT NULL,
                Help_type TEXT NOT NULL,
                Issue TEXT NOT NULL,
                Submitted_date TEXT NOT NULL,
                Status TEXT NOT NULL DEFAULT 'Open',
                FOREIGN KEY (Farmer_id) REFERENCES farmers(Farmer_id)
            )
        """)
        conn.commit()
        print("Help request table created successfully")
    except Exception as e:
        print(f"Error creating help request table: {e}")
    finally:
        conn.close()


def add_help_request(Farmer_id, Help_type, Issue, Submitted_date):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""
            INSERT INTO help_requests (Farmer_id, Help_type, Issue, Submitted_date)
            VALUES (?, ?, ?, ?)
        """, (Farmer_id, Help_type, Issue, Submitted_date))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error saving help request: {e}")
        return False
    finally:
        conn.close()


def get_all_help_requests():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT help_requests.Help_id, farmers.Farmer_id, farmers.Name,
                   farmers.Mobile, help_requests.Help_type, help_requests.Issue,
                   help_requests.Submitted_date, help_requests.Status
            FROM help_requests
            JOIN farmers ON help_requests.Farmer_id = farmers.Farmer_id
            ORDER BY help_requests.Help_id DESC
        """)
        return cursor.fetchall()
    finally:
        conn.close()


def get_help_request_by_id(Help_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Help_id, Farmer_id, Help_type, Issue, Status FROM help_requests WHERE Help_id=?",
            (Help_id,)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def update_help_request_status(Help_id, new_status):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE help_requests SET Status=? WHERE Help_id=?",
            (new_status, Help_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error updating help request: {e}")
        return False
    finally:
        conn.close()



def add_procurement(Farmer_id, Name, Procurement_token,
                    Procurement_date, Quantity, Crop):

    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            INSERT INTO procurements
            (Farmer_id, Name, Procurement_token,
             Procurement_date, Quantity, Crop, Status)
            VALUES (?, ?, ?, ?, ?, ?, 'Scheduled')
        """, (Farmer_id, Name, Procurement_token,
              Procurement_date, Quantity, Crop))

        conn.commit()
        print("Procurement added successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error adding procurement: {e}")
        return False

    finally:
        conn.close()


def add_procurement_request(Farmer_id, Name, Procurement_date, Quantity, Crop):
    """Save a farmer's request before the admin assigns a token and date."""
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(Procurement_id), 0) + 1 FROM procurements")
        next_id = cursor.fetchone()[0]
        request_token = "REQUEST-" + str(next_id)

        cursor.execute("""
            INSERT INTO procurements
            (Farmer_id, Name, Procurement_token, Procurement_date,
             Quantity, Crop, Status)
            VALUES (?, ?, ?, ?, ?, ?, 'Requested')
        """, (Farmer_id, Name, request_token, Procurement_date, Quantity, Crop))

        conn.commit()
        print("Procurement request saved successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error saving procurement request: {e}")
        return False

    finally:
        conn.close()


def update_procurement_schedule(Procurement_id, Procurement_token,
                                Procurement_date, new_status):
    """Let the admin assign a real token and date to a farmer's request."""
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE procurements
            SET Procurement_token=?, Procurement_date=?, Status=?
            WHERE Procurement_id=?
        """, (Procurement_token, Procurement_date, new_status, Procurement_id))

        if cursor.rowcount == 0:
            return False

        conn.commit()
        print("Procurement schedule updated successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating procurement schedule: {e}")
        return False

    finally:
        conn.close()


def get_procurement_by_id(Procurement_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM procurements WHERE Procurement_id=?",
            (Procurement_id,)
        )

        details = cursor.fetchall()

        if details:
            for detail in details:
                print(detail)
        else:
            print(f"No procurement found with ID {Procurement_id}")

        return details

    finally:
        conn.close()

def get_all_procurements():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM procurements")

        details = cursor.fetchall()

        for detail in details:
            print(detail)

        print(f"Total procurements retrieved: {len(details)}")
        return details

    finally:
        conn.close()

def get_procurement_by_farmer_id(Farmer_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM procurements WHERE Farmer_id=?",
            (Farmer_id,)
        )

        details = cursor.fetchall()

        if details:
            for detail in details:
                print(detail)
        else:
            print(f"No procurement found for Farmer ID {Farmer_id}")

        return details

    finally:
        conn.close()

def update_procurement_status(Procurement_id, new_status):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE procurements SET Status=? WHERE Procurement_id=?",
            (new_status, Procurement_id)
        )

        if cursor.rowcount == 0:
            print(f"No procurement found with ID {Procurement_id}")
            return False

        conn.commit()

        print("Now updated procurement details are:-")
        get_procurement_by_id(Procurement_id)

        print("Procurement status updated successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating procurement status: {e}")
        return False

    finally:
        conn.close()


def add_notification(Farmer_id, Name, Message, Sent_date, Status):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            INSERT INTO notifications
            (Farmer_id, Name, Message, Sent_date, Status)
            VALUES (?, ?, ?, ?, ?)
        """, (Farmer_id, Name, Message, Sent_date, Status))

        conn.commit()
        print("Notification added successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error adding notification: {e}")
        return False

    finally:
        conn.close()

def get_all_notifications():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM notifications")

        details = cursor.fetchall()

        for detail in details:
            print(detail)

        print(f"Total notifications retrieved: {len(details)}")
        return details

    finally:
        conn.close()

def get_notifications_by_farmer_id(Farmer_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM notifications WHERE Farmer_id=?",
            (Farmer_id,)
        )

        details = cursor.fetchall()

        if details:
            for detail in details:
                print(detail)
        else:
            print(f"No notifications found for Farmer ID {Farmer_id}")

        return details

    finally:
        conn.close()

def update_notification_status(Notification_id, new_status):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE notifications SET Status=? WHERE Notification_id=?",
            (new_status, Notification_id)
        )

        if cursor.rowcount == 0:
            print(f"No notification found with ID {Notification_id}")
            return False

        conn.commit()

        print("Now updated notification details are:-")

        get_notification_by_id(Notification_id)

        print("Notification status updated successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error updating notification status: {e}")
        return False

    finally:
        conn.close()


def get_notification_by_id(Notification_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM notifications WHERE Notification_id=?",
            (Notification_id,)
        )

        details = cursor.fetchall()

        if details:
            for detail in details:
                print(detail)
        else:
            print(f"No notification found with ID {Notification_id}")

        return details

    finally:
        conn.close()

def add_admin(Name, Mobile, Password_hash=None):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO admin (Name, Mobile, Password_hash)
            VALUES (?, ?, ?)
        """, (Name, Mobile, Password_hash))

        conn.commit()
        print("Admin inserted successfully")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error adding admin details: {e}")
        return False

    finally:
        conn.close()

def delete_admin(admin_id):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM admin
            WHERE admin_id = ?
        """, (admin_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("Admin deleted successfully")
            return True
        else:
            print("Admin not found")
            return False

    except Exception as e:
        conn.rollback()
        print(f"Error deleting admin: {e}")
        return False

    finally:
        conn.close()

def update_admin(admin_id, Name, Mobile):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE admin
            SET Name = ?, Mobile = ?
            WHERE admin_id = ?
        """, (Name, Mobile, admin_id))

        conn.commit()

        if cursor.rowcount > 0:
            print("Admin updated successfully")
            return True
        else:
            print("Admin not found")
            return False

    except Exception as e:
        conn.rollback()
        print(f"Error updating admin details: {e}")
        return False

    finally:
        conn.close()



def login_check(Mobile):
    conn = sqlite3.connect("database.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farmers WHERE Mobile=?", (Mobile,))
        data=cursor.fetchone()
        return data
    except Exception as e:
        print(f"error occur due to {e}")
    finally:
        conn.close()


def set_farmer_password(Mobile, Password_hash):
    conn = sqlite3.connect("database.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE farmers SET Password_hash = ? WHERE Mobile = ? AND Password_hash IS NULL",
            (Password_hash, Mobile)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def admin_table():
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Mobile INTEGER UNIQUE NOT NULL,
                Password_hash TEXT
            )
        """)

        conn.commit()
        print("Admin table created successfully")

    except Exception as e:
        print(f"Error creating table: {e}")

    finally:
        conn.close()

def admin_check(Mobile):
    conn = sqlite3.connect("database.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE Mobile=?", (Mobile,))
        data=cursor.fetchone()
        return data
    except Exception as e:
        print(f"error occur due to {e}")
    finally:
        conn.close()

# Initialize all database tables

def init_database():
    farmer_table()
    procurement_table()
    notification_table()
    help_request_table()
    admin_table()

    # Add password columns to databases created before login was added.
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(farmers)")
    farmer_columns = cursor.fetchall()
    if "Password_hash" not in [column[1] for column in farmer_columns]:
        cursor.execute("ALTER TABLE farmers ADD COLUMN Password_hash TEXT")

    cursor.execute("PRAGMA table_info(admin)")
    admin_columns = cursor.fetchall()
    if "Password_hash" not in [column[1] for column in admin_columns]:
        cursor.execute("ALTER TABLE admin ADD COLUMN Password_hash TEXT")

    # Older test records used Pending before the project statuses were finalized.
    cursor.execute("UPDATE procurements SET Status = 'Scheduled' WHERE Status = 'Pending'")

    conn.commit()
    conn.close()

    print("All database tables initialized successfully")


if __name__ == "__main__":
    init_database()
    debug = True
