import sqlite3
from datetime import date
from plyer import notification
import database


# Show a notification on the computer running this program.
def send_notification(message):
    try:
        notification.notify(
            title="FarmLink procurement update",
            message=message,
            app_name="Farmer E Connect",
            timeout=10
        )
    except Exception as e:
        # The database notification is already saved if the desktop popup is unavailable.
        print(f"Could not show desktop notification: {e}")


# Save a notification for one farmer in the database.
def notify_one_farmer(farmer_id, message):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Name FROM farmers WHERE Farmer_id = ?",
            (farmer_id,)
        )
        farmer = cursor.fetchone()

        if farmer is None:
            print(f"No farmer found with ID {farmer_id}")
            return False

        sent_date = date.today().isoformat()
        result = database.add_notification(
            farmer_id, farmer[0], message, sent_date, "Sent"
        )

        if result:
            print(f"Notification saved for {farmer[0]}")
            send_notification(message)
            return True

        return False

    finally:
        conn.close()


# Save the same notification for every farmer.
def notify_all_farmers(message):
    conn = sqlite3.connect("database.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Farmer_id, Name FROM farmers")
        farmers = cursor.fetchall()

        if len(farmers) == 0:
            print("There are no farmers to notify")
            return False

        sent_date = date.today().isoformat()
        saved_count = 0

        for farmer in farmers:
            result = database.add_notification(
                farmer[0], farmer[1], message, sent_date, "Sent"
            )

            if result:
                saved_count = saved_count + 1

        print(f"Notification saved for {saved_count} farmers")

        if saved_count > 0:
            send_notification(message)
            return True

        return False

    finally:
        conn.close()

if __name__=="__main__":
    debug=True
