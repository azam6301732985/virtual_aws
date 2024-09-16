from flask import Flask, request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

# Use a simple temporary key for development purposes (do not use in production)
app.secret_key = 'temporary_key'

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='database-2.c5eyis2co1ux.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='azam_1234',
        database='course_app'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password using werkzeug's generate_password_hash
        hashed_password = generate_password_hash(password, method='sha256')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # If user exists and password matches
        if result and check_password_hash(result[0], password):
            return redirect(url_for('content'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')



@app.route('/content')
def content():
    # List of URLs for course materials
    course_urls = [
        'https://aws-project-virtualclassroom.s3.ap-south-1.amazonaws.com/python_code.pdf',
        'https://aws-project-virtualclassroom.s3.ap-south-1.amazonaws.com/PYTHON+PROGRAMMING+NOTES.pdf'
    ]
    
    return render_template('content.html', course_urls=course_urls)


if __name__ == '__main__':
    app.run(debug=True)
