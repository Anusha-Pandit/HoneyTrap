import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure PostgreSQL database using .env values
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the LoginAttempt model
class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    ip_address = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Create the database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created or already exist.")
    except Exception as e:
        print(f"Error connecting to or creating database tables: {e}")
        print("Please ensure your PostgreSQL server is running and the connection string is correct.")

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr

        try:
            login_attempt = LoginAttempt(username=username, password=password, ip_address=ip_address)
            db.session.add(login_attempt)
            db.session.commit()
            flash('Invalid username or password', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving login attempt: {e}', 'error')
            print(f"Database error on login attempt: {e}")

        return redirect(url_for('login'))

    return render_template('login.html')

# Route for the logs page
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    if request.method == 'POST':
        admin_password = request.form['admin_password']
        if admin_password == 'admin123':
            try:
                login_attempts = LoginAttempt.query.all()
                return render_template('logs.html', login_attempts=login_attempts)
            except Exception as e:
                flash(f'Error retrieving logs: {e}', 'error')
                print(f"Database error retrieving logs: {e}")
                return redirect(url_for('logs'))
        else:
            flash('Invalid admin password', 'error')
            return redirect(url_for('logs'))

    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)


# to run on localhost: http://127.0.0.1:5000
