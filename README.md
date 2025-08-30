# Cybersecurity Honeypot

A simple cybersecurity honeypot project built with Flask and PostgreSQL.

## Project Overview

This project creates a fake login page that captures and stores login attempts in a PostgreSQL database. It includes a protected route to view all captured login attempts.

## Setup Instructions

1. Install Python dependencies:
   ```
   pip install flask flask-sqlalchemy psycopg2-binary
   ```

2. Configure PostgreSQL:
   - Create a database named `honeypot_db`
   - Update the database URI in `app.py` with your PostgreSQL credentials

3. Run the Flask app:
   ```
   python app.py
   ```

## Database Schema

The database schema is automatically created by SQLAlchemy. The `login_attempts` table has the following fields:
- `id` (Integer, Primary Key)
- `username` (String)
- `password` (String)
- `ip_address` (String)
- `timestamp` (DateTime)

## Security Note

This is a demo honeypot project for learning purposes only. It is not intended for production use and does not provide real security. Always follow best practices for security and privacy.
