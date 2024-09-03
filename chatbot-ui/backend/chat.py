import re
import random
import sqlite3

# Database connection function
def connect_db():
    return sqlite3.connect('chatbot.db')

# Function to add or update user information in the database
def add_or_update_user(name, preference=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()
    
    if user:
        if preference:
            cursor.execute('UPDATE users SET preference = ? WHERE name = ?', (preference, name))
    else:
        cursor.execute('INSERT INTO users (name, preference) VALUES (?, ?)', (name, preference))
    
    conn.commit()
    conn.close()

# Function to retrieve user information
def get_user(name):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def chatbot_response(user_input, context):
    user_input = user_input.lower()
    
    # Handle asking for and storing name
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
            add_or_update_user(context['name'], preference)
            return f"Got it! I've updated your preference to {preference}."
        else:
            context['ask_name'] = True
            return "I need to know your name first! What's your name?"
    elif re.search(r'what is my preference', user_input):
        if 'name' in context:
            user = get_user(context['name'])
            if user and user[2]:
                return f"Your current preference is: {user[2]}"
            else:
                return "I don't have any preferences saved for you."
        else:
            context['ask_name'] = True
            return "I need to know your name first! What's your name?"
    elif re.search(r'bye|exit|quit', user_input):
        return "Goodbye! Have a nice day!"
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

def chat():
    print("Chatbot: Hello! I'm here to chat with you. Type 'exit' to end the chat.")
    context = {}
    while True:
        user_input = input("You: ")
        response = chatbot_response(user_input, context)
        print(f"Chatbot: {response}")
        
        if re.search(r'bye|exit|quit', user_input.lower()):
            break

chat()
