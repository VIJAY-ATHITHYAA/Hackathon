from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from llm_utils import generate_fitness_plan

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ MySQL Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="healthmate"
    )

# ✅ Home
@app.route('/')
def home():
    return render_template('home.html')

# ✅ Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        regno = request.form['regno']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (regno, email, password) VALUES (%s, %s, %s)", (regno, email, password))
        db.commit()
        db.close()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        regno = request.form['regno']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE regno = %s", (regno,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = user['regno']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# ✅ Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

# ✅ Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ✅ DeepSeek-powered AI Symptom Checker
def query_openrouter(symptoms):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-70b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a highly intelligent medical assistant. Given symptoms, provide possible conditions, risks, and general advice. Be specific and concise."
            },
            {
                "role": "user",
                "content": symptoms
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process that. Please try again."

@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():
    result = None
    if request.method == 'POST':
        symptoms = request.form['symptoms']
        result = query_openrouter(symptoms)
    return render_template('symptom_checker.html', result=result)

# ✅ TinyLlama-powered Fitness ChatBot
@app.route('/fitness', methods=['GET', 'POST'])
def fitness():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['conversation'].append(('You', user_input))

        try:
            bot_response = generate_fitness_plan(user_input)
        except Exception as e:
            bot_response = "Oops! Something went wrong."

        session['conversation'].append(('Bot', bot_response))
    
    return render_template('fitness.html', conversation=session['conversation'])

@app.route('/reset_fitness')
def reset_fitness():
    session.pop('fitness', None)
    return redirect(url_for('fitness'))

# ✅ Run App
if __name__ == '__main__':
    app.run(debug=True)
