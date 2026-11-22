from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import database
import farmer
import admin
import notification
import analytics


app = Flask(__name__)

# Flask uses this key to remember the logged-in user between pages.
app.secret_key = "farmer-e-connect-demo-key"

# Create the tables if they do not already exist.
database.init_database()


# The CSS file is inside the templates folder in this project.
@app.route("/style.css")
def style():
    return send_from_directory(app.root_path + "/templates", "style.css")


# Show the home page.
@app.route("/")
def first_page():
    return render_template("index.html")


# Show the registration form, then save the farmer when it is submitted.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        village = request.form.get("village", "").strip()
        village_pin = request.form.get("village_pin", "").strip()
        crop = request.form.get("crop", "").strip()
        password = request.form.get("password", "")

        if not name:
            return render_template("register.html", message="Enter your name.")
        if not mobile:
            return render_template("register.html", message="Enter your mobile number.")
        if not village:
            return render_template("register.html", message="Enter your village.")
        if not village_pin:
            return render_template("register.html", message="Enter your village PIN code.")
        if not crop:
            return render_template("register.html", message="Enter your crop.")
        if not password:
            return render_template("register.html", message="Create a password.")

        # Save a password hash so the original password is not stored in the database.
        password_hash = generate_password_hash(password)
        result = farmer.register_farmer(
            name, mobile, village, village_pin, crop, password_hash
        )

        if result:
            if session.get("role") == "admin":
                return redirect(url_for("admin_dashboard"))

            return render_template(
                "login.html",
                message="Registration complete. Log in with your mobile number and password."
            )

        return render_template(
            "register.html",
            message="That mobile number may already be registered."
        )

    return render_template("register.html")


# Check a farmer's details and remember them after a successful login.
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form.get("mobile", "").strip()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        farmer_record = farmer.login_check(mobile)

        if farmer_record is not None:
            saved_name = farmer_record[1]
            saved_password_hash = farmer_record[6]

            if saved_name == name and saved_password_hash:
                if check_password_hash(saved_password_hash, password):
                    session.clear()
                    session["role"] = "farmer"
                    session["farmer_id"] = farmer_record[0]
                    session["farmer_name"] = farmer_record[1]
                    return redirect(url_for("farmer_dashboard"))

        return render_template(
            "login.html",
            message="Mobile number, name, or password is incorrect."
        )

    return render_template("login.html")


# Let an existing farmer set a password for an older account.
@app.route("/activate_farmer", methods=["GET", "POST"])
def activate_farmer():
    if request.method == "POST":
        mobile = request.form.get("mobile", "").strip()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        farmer_record = farmer.login_check(mobile)

        if farmer_record is not None:
            saved_name = farmer_record[1]
            saved_password_hash = farmer_record[6]

            if saved_name == name and saved_password_hash is None and password:
                password_hash = generate_password_hash(password)
                result = farmer.activate_farmer(mobile, password_hash)

                if result:
                    return render_template(
                        "login.html",
                        message="Password set. You can now log in."
                    )

        return render_template(
            "activate_farmer.html",
            message="Could not activate this account. Check the name and mobile number, or try logging in."
        )

    return render_template("activate_farmer.html")


# Show a farmer's procurement records and notifications on their dashboard.
@app.route("/farmer_dashboard")
def farmer_dashboard():
    if session.get("role") != "farmer":
        return redirect(url_for("login"))

    farmer_id = session["farmer_id"]
    farmer_records = database.get_details_by_id(farmer_id)

    if not farmer_records:
        session.clear()
        return redirect(url_for("login"))

    procurement_records = database.get_procurement_by_farmer_id(farmer_id)
    notification_records = database.get_notifications_by_farmer_id(farmer_id)

    scheduled_count = 0
    delayed_count = 0
    completed_count = 0
    requested_count = 0
    dashboard_requests = []

    # Each procurement row contains its ID, farmer, token, date, quantity, crop, and status.
    for record in procurement_records:
        if record[7] == "Scheduled":
            scheduled_count = scheduled_count + 1
        elif record[7] == "Requested":
            requested_count = requested_count + 1
        elif record[7] == "Delayed":
            delayed_count = delayed_count + 1
        elif record[7] == "Completed":
            completed_count = completed_count + 1

        request_details = {
            "id": record[0],
            "token_number": record[3],
            "procurement_date": record[4],
            "crop": record[6],
            "quantity": record[5],
            "status": record[7]
        }
        dashboard_requests.append(request_details)

    dashboard_notifications = []
    for record in notification_records:
        notification_details = {
            "message": record[3],
            "sent_date": record[4]
        }
        dashboard_notifications.append(notification_details)

    # JavaScript in the dashboard uses this information to fill the page.
    dashboard_data = {
        "total_requests": len(procurement_records),
        "requested_requests": requested_count,
        "scheduled_requests": scheduled_count,
        "delayed_requests": delayed_count,
        "completed_requests": completed_count,
        "recent_requests": dashboard_requests,
        "recent_notifications": dashboard_notifications
    }

    return render_template(
        "farmer_dashboard.html",
        farmer_name=farmer_records[0][1],
        farmer_id=farmer_records[0][0],
        dashboard_data=dashboard_data
    )


# Log the farmer out.
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Show the admin registration form, then save the admin account.
@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not mobile or not password:
            return render_template(
                "admin_resister.html",
                message="Please complete every field."
            )

        if password != confirm_password:
            return render_template(
                "admin_resister.html",
                message="The passwords do not match."
            )

        password_hash = generate_password_hash(password)
        result = admin.add_admin(name, mobile, password_hash)

        if result:
            return render_template(
                "admin_login.html",
                message="Admin registered. You can now log in."
            )

        return render_template(
            "admin_resister.html",
            message="That mobile number may already be registered."
        )

    return render_template("admin_resister.html")


# Check an admin's details and remember them after a successful login.
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        mobile = request.form.get("mobile", "").strip()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "")
        admin_record = admin.admin_check(mobile)

        if admin_record is not None:
            saved_name = admin_record[1]
            saved_password_hash = admin_record[3]

            if saved_name == name and saved_password_hash:
                if check_password_hash(saved_password_hash, password):
                    session.clear()
                    session["role"] = "admin"
                    session["admin_name"] = admin_record[1]
                    return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            message="Mobile number, name, or password is incorrect."
        )

    return render_template("admin_login.html")


# Turn the one-cell Pandas result into a regular Python number for the page.
def get_report_count(report):
    if report is None:
        return 0

    count = report.iloc[0, 0]
    return int(count)


# Check whether the current visitor is logged in as an admin.
def admin_is_logged_in():
    if session.get("role") == "admin":
        return True
    return False


# Show totals and recent procurement records on the admin dashboard.
@app.route("/admin_dashboard")
def admin_dashboard():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    farmer_records = database.get_all_details()
    procurement_records = database.get_all_procurements()
    help_requests = database.get_all_help_requests()
    dashboard_records = []
    requested_count = 0

    for record in procurement_records:
        if record[7] == "Requested":
            requested_count = requested_count + 1
        record_details = {
            "token_number": record[3],
            "farmer_id": record[1],
            "crop": record[6],
            "procurement_date": record[4],
            "quantity": record[5],
            "status": record[7]
        }
        dashboard_records.append(record_details)

    dashboard_data = {"recent_records": dashboard_records}

    completed_report = analytics.get_procurement_status_completed()
    scheduled_report = analytics.get_procurement_status_scheduled()
    delayed_report = analytics.get_procurement_status_delayed()
    cancelled_report = analytics.get_procurement_status_cancelled()

    return render_template(
        "admin_dashboard.html",
        total_farmers=len(farmer_records),
        total_procurement=len(procurement_records),
        help_request_count=len(help_requests),
        requested_count=requested_count,
        completed_count=get_report_count(completed_report),
        scheduled_count=get_report_count(scheduled_report),
        delayed_count=get_report_count(delayed_report),
        cancelled_count=get_report_count(cancelled_report),
        dashboard_data=dashboard_data
    )


# The admin uses the farmer registration form to add a farmer.
@app.route("/add_farmer")
def add_farmer():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))
    return redirect(url_for("register"))


# Show all farmers to the admin.
@app.route("/view_farmers")
def view_farmers():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    farmer_records = database.get_all_details()
    return render_template("admin_farmers.html", farmers=farmer_records)


# Procurement requests are submitted by farmers. Send the admin to the request list.
@app.route("/add_procurement", methods=["GET", "POST"])
def add_procurement():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))
    return redirect(url_for("view_procurements"))


# Show procurement records to the admin.
@app.route("/view_procurements")
def view_procurements():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    procurement_records = database.get_all_procurements()
    return render_template("admin_procurements.html", records=procurement_records)


# Save a new status chosen by the admin.
@app.route("/update_status/<int:procurement_id>", methods=["POST"])
def update_status(procurement_id):
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    new_status = request.form.get("status", "")

    token = request.form.get("token_number", "").strip()
    procurement_date = request.form.get("procurement_date", "").strip()

    procurement_records = database.get_procurement_by_id(procurement_id)
    if not procurement_records:
        return redirect(url_for("view_procurements"))

    procurement_record = procurement_records[0]
    farmer_id = procurement_record[1]

    if token and procurement_date:
        if new_status == "Scheduled" or new_status == "Delayed" or new_status == "Completed" or new_status == "Cancelled":
            result = database.update_procurement_schedule(
                procurement_id, token, procurement_date, new_status
            )
            if result:
                message = (
                    "Your procurement request is now " + new_status
                    + ". Token: " + token + ". Date: " + procurement_date + "."
                )
                notification.notify_one_farmer(farmer_id, message)
        return redirect(url_for("view_procurements"))

    if new_status == "Scheduled" or new_status == "Delayed":
        result = database.update_procurement_status(procurement_id, new_status)
    elif new_status == "Completed" or new_status == "Cancelled":
        result = database.update_procurement_status(procurement_id, new_status)
    else:
        result = False

    if result:
        message = (
            "Your procurement status was updated to " + new_status
            + ". Token: " + procurement_record[3]
            + ". Date: " + procurement_record[4] + "."
        )
        notification.notify_one_farmer(farmer_id, message)

    return redirect(url_for("view_procurements"))


# Save a message for one farmer or for all farmers.
@app.route("/admin_notifications", methods=["GET", "POST"])
def admin_notifications():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    farmer_records = database.get_all_details()
    message = ""

    if request.method == "POST":
        farmer_id = request.form.get("farmer_id", "")
        notification_message = request.form.get("message", "").strip()

        if not notification_message:
            message = "Enter a notification message."
        elif farmer_id == "all":
            notification.notify_all_farmers(notification_message)
            message = "Notification saved for all farmers."
        elif farmer_id:
            notification.notify_one_farmer(farmer_id, notification_message)
            message = "Notification saved for the selected farmer."
        else:
            message = "Choose a farmer."

    notification_records = database.get_all_notifications()

    return render_template(
        "admin_notifications.html",
        farmers=farmer_records,
        notifications=notification_records,
        message=message
    )


# Show farmers' help requests and send a reply to a farmer.
@app.route("/admin_helpdesk", methods=["GET", "POST"])
def admin_helpdesk():
    if not admin_is_logged_in():
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        help_id = request.form.get("help_id", "")
        reply = request.form.get("reply", "").strip()

        if not reply:
            return redirect(url_for("admin_helpdesk", message="Write a reply before sending."))

        help_request = database.get_help_request_by_id(help_id)
        if not help_request:
            return redirect(url_for("admin_helpdesk", message="Help request not found."))

        sent = notification.notify_one_farmer(
            help_request[1],
            "Reply to your help request: " + reply
        )

        if sent:
            database.update_help_request_status(help_id, "Responded")
            return redirect(url_for("admin_helpdesk", message="Reply sent to the farmer."))

        return redirect(url_for("admin_helpdesk", message="Could not save the reply."))

    return render_template(
        "admin_helpdesk.html",
        help_requests=database.get_all_help_requests(),
        message=request.args.get("message", "")
    )


# Log the admin out.
@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# These links return to the farmer dashboard sections.
@app.route("/farmer_profile")
@app.route("/my_crops")
@app.route("/my_procurement")
@app.route("/notifications")
def farmer_dashboard_links():
    return redirect(url_for("farmer_dashboard"))


# Let the farmer submit a request for the admin to schedule.
@app.route("/apply_procurement", methods=["GET", "POST"])
def apply_procurement():
    if session.get("role") != "farmer":
        return redirect(url_for("login"))

    farmer_records = database.get_details_by_id(session["farmer_id"])
    if not farmer_records:
        session.clear()
        return redirect(url_for("login"))

    farmer_record = farmer_records[0]

    if request.method == "POST":
        quantity = request.form.get("quantity", "").strip()
        requested_date = request.form.get("procurement_date", "").strip()

        if not quantity or not requested_date:
            return render_template(
                "apply_procurement.html",
                crop=farmer_record[5],
                requested_date=requested_date,
                message="Enter both the quantity and your preferred procurement date."
            )

        try:
            quantity = float(quantity)
        except ValueError:
            return render_template(
                "apply_procurement.html",
                crop=farmer_record[5],
                requested_date=requested_date,
                message="Enter a valid quantity."
            )

        if quantity <= 0:
            return render_template(
                "apply_procurement.html",
                crop=farmer_record[5],
                requested_date=requested_date,
                message="Quantity must be greater than zero."
            )

        result = database.add_procurement_request(
            farmer_record[0], farmer_record[1], requested_date, quantity, farmer_record[5]
        )

        if result:
            return redirect(url_for("farmer_dashboard") + "#procurement")

        return render_template(
            "apply_procurement.html",
            crop=farmer_record[5],
            requested_date=requested_date,
            message="Could not save your request. Please try again."
        )

    return render_template("apply_procurement.html", crop=farmer_record[5])


# Take the farmer to the MSP rates section on the home page.
@app.route("/msp_rates")
def msp_rates():
    return redirect(url_for("first_page") + "#rates")


# Show the help form and a simple confirmation after it is submitted.
@app.route("/help", methods=["GET", "POST"])
def help_page():
    if request.method == "POST":
        farmer_name = request.form.get("farmer_name", "").strip()
        farmer_id = request.form.get("farmer_id", "").strip()
        help_type = request.form.get("help_type", "").strip()
        issue = request.form.get("issue", "").strip()

        if not farmer_name or not farmer_id or not help_type or not issue:
            return render_template("help.html", message="Please complete every field.")

        farmer_records = database.get_details_by_id(farmer_id)
        if not farmer_records or farmer_records[0][1].lower() != farmer_name.lower():
            return render_template("help.html", message="Check your farmer name and ID.")

        result = database.add_help_request(
            farmer_records[0][0], help_type, issue, date.today().isoformat()
        )

        if result:
            return render_template("help.html", message="Your help request was sent to the admin.")

        return render_template("help.html", message="Could not save your request. Please try again.")
    return render_template("help.html")


if __name__ == "__main__":
    # Use port 5001 because an older server is still holding port 5000.
    app.run(debug=True, port=5001)

