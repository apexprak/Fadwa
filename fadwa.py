from flask import Flask, request, render_template_string, redirect, url_for, send_file
import os

app = Flask(__name__)

# Path to the file where attendance will be saved
ATTENDANCE_FILE = 'attendance.txt'

# Function to save a name to the file, with UTF-8 encoding
def save_name(name):
    with open(ATTENDANCE_FILE, 'a', encoding='utf-8') as f:
        f.write(name + '\n')

# Function to load names from the file, with UTF-8 encoding
def load_names():
    try:
        with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
            names = f.read().splitlines()
    except FileNotFoundError:
        names = []
    return names

@app.route('/')
def index():
    student_names = load_names()
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Attendance Tracker</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f4f9;
            }
            .container {
                text-align: center;
                width: 300px;
                padding: 20px;
                background: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h1 {
                color: #333;
                margin-bottom: 20px;
            }
            form {
                margin-bottom: 20px;
            }
            input[type="text"] {
                width: 80%;
                padding: 8px;
                margin-right: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                padding: 8px 12px;
                border: none;
                color: #fff;
                background-color: #007bff;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            h2 {
                color: #333;
                margin-top: 20px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                padding: 5px 0;
                color: #555;
            }
            header {
                font-size: 24px;
                color: #007bff;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>Fadwa</header>
            <h1>Attendance Tracker</h1>
            <form action="{{ url_for('add_student') }}" method="POST">
                <input type="text" name="name" placeholder="Enter your name" required>
                <button type="submit">Submit</button>
            </form>
            <h2>Attendance List:</h2>
            <ul>
                {% for name in student_names %}
                    <li>{{ name }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    ''', student_names=student_names)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    if name.lower() == 'katame':
        # If "katame" is entered, download the attendance file
        if os.path.exists(ATTENDANCE_FILE):
            return send_file(ATTENDANCE_FILE, as_attachment=True)
        else:
            return "Attendance file not found.", 404
    else:
        # Save the name and redirect to index
        save_name(name)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
