import re
import random

def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Define responses
    greetings = ["Hello! How can I help you today?", "Hi there! What do you need?", "Hey! What's up?"]
    
    if re.search(r'hello|hi|hey', user_input):
        return random.choice(greetings)
    elif re.search(r'how are you|how do you do', user_input):
        return "I'm just a bot, but I'm doing great! How about you?"
    elif re.search(r'what is your name|who are you', user_input):
        return "I'm a simple chatbot created to chat with you!"
    elif re.search(r'thank you|thanks', user_input):
        return "You're welcome! Do you have any other questions?"
    elif re.search(r'bye|exit|quit', user_input):
        return "Goodbye! Have a nice day!"
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

def chat():
    print("Chatbot: Hello! I'm here to chat with you. Type 'exit' to end the chat.")
    while True:
        user_input = input("You: ")
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")
        
        if re.search(r'bye|exit|quit', user_input.lower()):
            break

chat()
