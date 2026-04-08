import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def process_chat(user_message: str, tournaments_context: list):
    """
    Calls Google Gemini AI to assist the user based on the available tournaments.
    """
    if not api_key:
        return "Error: GOOGLE_API_KEY not found in environment variables. Please add it to your .env file."
    
    # Format tournaments for the prompt
    context_str = "Available Tournaments:\n"
    if not tournaments_context:
        context_str += "No tournaments available right now.\n"
    for t in tournaments_context:
        context_str += f"- ID: {t.id}, Title: '{t.title}', Sport: {t.sport}, Location: {t.location}, Entry Fee: {t.entry_fee}, Prize Pool: {t.prize_pool}, Date: {t.tournament_date}. Desc: {t.description}\n"

    system_prompt = f"""
    You are a highly helpful Local Sports Tournament Discovery Assistant. 
    Your goal is to help players find relevant sports tournaments. 
    You have access to the following real-time data about available tournaments:
    
    {context_str}
    
    Answer the user's queries based ONLY on the tournament data provided above. 
    If they ask for something not in the data, tell them you don't have that information right now. 
    Be enthusiastic, friendly, and concise. Format your response cleanly.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            contents=[system_prompt, f"User Query: {user_message}"]
        )
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error while processing your request: {str(e)}"
