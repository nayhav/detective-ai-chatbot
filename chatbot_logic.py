import os
from dotenv import load_dotenv
from case_data import CASE_DETAILS
from google.generativeai import GenerativeModel, configure

load_dotenv()

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Error: Gemini API key not found. Check .env file.")

# Configure Gemini AI Model
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.0-flash')

# In-memory session store (for user context)
user_sessions = {}

def ask_gemini(user_id, user_input):
    """Sends a query to Gemini AI with case context and user memory."""
    
    # Retrieve or initialize conversation history
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    conversation_history = user_sessions[user_id]
    conversation_history.append(f"User: {user_input}")

    try:
        prompt = f"""
        You are a detective AI assisting in a murder investigation.
        Your job is to analyze evidence, suspects, and clues.
        You must only answer questions related to the murder case.

        If the user asks anything unrelated, reply:
        "Detective, stay focused! We have a case to solve."

        Case Details:
        - Victim: {CASE_DETAILS['victim']}
        - Crime Scene: {CASE_DETAILS['crime_scene']}
        - Time of Death: {CASE_DETAILS['time_of_death']}
        - Suspects: {', '.join(CASE_DETAILS['suspects'].keys())}
        - Clues: {', '.join(CASE_DETAILS['clues'].keys())}

        Previous Conversation:
        {chr(10).join(conversation_history[-5:])}

        User Inquiry:
        "{user_input}"
        """

        response = model.generate_content(prompt)

        # Handle API response properly
        if not response or not hasattr(response, "text") or not response.text:
            return {"response": "Sorry, I'm having trouble processing that. Try again."}

        ai_reply = response.text.strip()
        conversation_history.append(f"AI: {ai_reply}")

        # Limit history to last 20 messages
        user_sessions[user_id] = conversation_history[-20:]

        return {"response": ai_reply}  # Always return a JSON object

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return {"response": f"Error: {e}"}  # Return JSON instead of None

def get_intro():
    """Returns the introduction to the mystery."""
    return {
        "message": f"Detective, a murder has occurred!\n\n"
                   f"Victim: {CASE_DETAILS['victim']}\n"
                   f"Scene: {CASE_DETAILS['crime_scene']}\n"
                   f"Time of Death: {CASE_DETAILS['time_of_death']}\n\n"
                   f"Your task: Identify the killer!"
    }

def get_suspect_info():
    """Returns a formatted list of suspects."""
    suspects = "\n".join([f"- {s}: {desc}" for s, desc in CASE_DETAILS['suspects'].items()])
    return {"message": f"Suspects:\n{suspects}"}

def get_clues():
    """Returns discovered clues."""
    clues = "\n".join([f"- {c}: {desc}" for c, desc in CASE_DETAILS['clues'].items()])
    return {"message": f"Clues found:\n{clues}"}

def get_response(user_id, user_input):
    """Handles user input and provides appropriate responses."""
    user_input = user_input.lower().strip()

    if user_input in ["hello", "hi", "hey", "yo", "greetings"]:
        return {"response": "Hello, Detective! Ready to crack the case?"}
    elif "suspect" in user_input:
        return get_suspect_info()
    elif "victim" in user_input:
        return {"response": f"The victim was {CASE_DETAILS['victim']}, found in {CASE_DETAILS['crime_scene']}."}
    elif "clues" in user_input:
        return get_clues()
    else:
        
        return ask_gemini(user_id, user_input)
