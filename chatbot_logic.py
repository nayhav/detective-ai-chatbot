# chatbot_logic.py
import os
print(os.getcwd())
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
from case_data import CASE_DETAILS  


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


from google.generativeai import GenerativeModel, configure
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.0-flash')

def ask_gemini(user_input):
    """Sends a query to Gemini AI with a strict detective context."""
    try:
        prompt = f"""
        You are a detective AI assisting in a murder investigation.
        Your job is to help analyze evidence, suspects, and clues.
        You **must only** answer questions related to the murder case.

        If the user asks anything unrelated (e.g., sports, general trivia, weather), reply:
        "Detective, stay focused! We have a case to solve."

        Case Details:
        - Victim: {CASE_DETAILS['victim']}
        - Crime Scene: {CASE_DETAILS['crime_scene']}
        - Time of Death: {CASE_DETAILS['time_of_death']}
        - Suspects: {', '.join(CASE_DETAILS['suspects'].keys())}
        - Clues: {', '.join(CASE_DETAILS['clues'].keys())}

        User Inquiry:
        "{user_input}"
        """

        response = model.generate_content(prompt) 

        if hasattr(response, "text"):
            return response.text.strip()
        else:
            return "Gemini responded, but no text was found"

    except Exception as e:
        print(f"Full Gemini API Error: {e}") 
        return f"Error: {e}"

def get_intro():
    """Returns the introduction to the mystery."""
    return f"Detective, a murder has occurred!\n\nVictim: {CASE_DETAILS['victim']}\nScene: {CASE_DETAILS['crime_scene']}\nTime of Death: {CASE_DETAILS['time_of_death']}\n\nYour task: Identify the killer!"

def get_suspect_info():
    """Returns a formatted list of suspects."""
    suspects = "\n".join([f"- {s}: {desc}" for s, desc in CASE_DETAILS['suspects'].items()])
    return f"Suspects:\n{suspects}"

def get_clues():
    """Returns discovered clues."""
    clues = "\n".join([f"- {c}: {desc}" for c, desc in CASE_DETAILS['clues'].items()])
    return f"Clues found:\n{clues}"

def get_response(user_input):
    """Handles user input and provides appropriate responses."""
    responses = {
        "hello": "Hello, Detective! How can I assist you in solving this case?",
        "who is the suspect": get_suspect_info(),
        "who was the victim": f"The victim was {CASE_DETAILS['victim']}, found dead in {CASE_DETAILS['crime_scene']}.",
        "what clues do we have?": get_clues(),
        "default": "I'm not sure about that. Try asking about the suspects or evidence."
    }

    if user_input.lower() in responses:
        return responses[user_input.lower()]
    else:
    
        return ask_gemini(user_input)

print(f"API Key: {GEMINI_API_KEY}") 
