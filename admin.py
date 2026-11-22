import database
import analytics
import notification
from farmer import add_procurement, register_farmer


# Display all farmers in the terminal.
def view_all_farmers():
    database.get_all_details()


# Display all procurement records in the terminal.
def view_all_procurements():
    database.get_all_procurements()


# Change the status of one procurement record.
def change_procurement_status(procurement_id, new_status):
    database.update_procurement_status(procurement_id, new_status)


# Save a notification for one farmer and show the local computer pop-up.
def send_farmer_notification(farmer_id, message):
    notification.notify_one_farmer(farmer_id, message)


# Save the same notification for every farmer and show a local computer pop-up.
def send_all_farmers_notification(message):
    notification.notify_all_farmers(message)


# Display the total registered farmer count using the Pandas report function.
def show_total_farmers():
    total = analytics.get_total_farmers()
    print(total)

#to varify admin

def admin_check(mobile):
    return database.admin_check(mobile)

def add_admin(Name, Mobile, password_hash=None):
    return database.add_admin(Name, Mobile, password_hash)

def delete_admin(admin_id):
    database.delete_admin(admin_id)

def update_admin(admin_id, Name, Mobile):
    database.update_admin(admin_id, Name, Mobile)

if __name__ == "__main__":
    debug = True
