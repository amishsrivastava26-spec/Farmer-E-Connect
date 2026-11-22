# Farmer E Connect

A beginner-friendly Flask project for farmers and procurement centre admins to track crop procurement and communicate about requests.

## Features

- Farmer registration, login, and dashboard.
- Farmers can request crop procurement, view their procurement status, and check MSP rates.
- Farmers can submit help requests and view admin replies and notifications.
- Admins can review farmer and procurement records, update procurement status, and respond to help requests.
- SQLite stores project data in `database.db`; Pandas provides procurement summaries.

## Run locally

1. Install Python 3.
2. Open a terminal in the project folder (`Farmer Queue`).
3. Install the required packages:

   ```bash
   pip install Flask pandas plyer
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open **http://127.0.0.1:5001** in your browser. The database tables are initialized when the app starts.

Admins can register or log in from the admin links on the site. Farmers can register and log in from the home page.
