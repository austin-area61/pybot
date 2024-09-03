from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('chatbot.db')

# Function to add or update user in the database
def add_or_update_user(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()

    if not user:
        cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))

    conn.commit()
    conn.close()

# Function to add a preference for a user
def add_preference(name, preference):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute('INSERT INTO preferences (user_id, preference) VALUES (?, ?)', (user_id, preference))

    conn.commit()
    conn.close()

# Function to get all preferences for a user
def get_preferences(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute('SELECT preference FROM preferences WHERE user_id = ?', (user_id,))
        preferences = cursor.fetchall()
        return [pref[0] for pref in preferences]

    conn.close()
    return []

# Function to generate chatbot responses
def chatbot_response(user_input, context):
    user_input = user_input.lower()

    if 'ask_name' in context:
        name = user_input.capitalize()
        add_or_update_user(name)
        context['name'] = name
        context.clear()
        return f"Nice to meet you, {name}! How can I help you today?"

    if re.search(r'hello|hi|hey', user_input):
        if 'name' in context:
            return f"Hello again, {context['name']}! How can I assist you?"
        else:
            context['ask_name'] = True
            return "Hello! What's your name?"
    elif re.search(r'set preference to (.+)', user_input):
        if 'name' in context:
            preference = re.findall(r'set preference to (.+)', user_input)[0]
            add_preference(context['name'], preference)
            return f"Got it! I've added your preference: {preference}."
        else:
            context['ask_name'] = True
            return "I need to know your name first! What's your name?"
    elif re.search(r'what are my preferences', user_input):
        if 'name' in context:
            preferences = get_preferences(context['name'])
            if preferences:
                return f"Your preferences are: {', '.join(preferences)}"
            else:
                return "I don't have any preferences saved for you."
        else:
            context['ask_name'] = True
            return "I need to know your name first! What's your name?"
    elif re.search(r'bye|exit|quit', user_input):
        return "Goodbye! Have a nice day!"
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Define a route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    context = data.get('context', {})
    
    response = chatbot_response(user_input, context)
    return jsonify({"response": response, "context": context})

if __name__ == '__main__':
    app.run(debug=True)
