import streamlit as st
import requests
import datetime

# --- Backend API URL ---
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Sport Connect", page_icon="🏆", layout="wide")

# Custom CSS for better UI (Glassmorphism & Gradients)
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Inter', sans-serif;
    }
    .tournament-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease;
    }
    .tournament-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .sport-tag {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .prize-tag {
        color: #4ade80;
        font-weight: bold;
    }
    .location-text {
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def fetch_tournaments(sport=None, location=None):
    params = {}
    if sport: params['sport'] = sport
    if location: params['location'] = location
    try:
        response = requests.get(f"{BACKEND_URL}/tournaments/", params=params)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
    return []

def register_player(tournament_id, name, email, team):
    payload = {
        "tournament_id": tournament_id,
        "player_name": name,
        "player_email": email,
        "team_name": team
    }
    try:
        response = requests.post(f"{BACKEND_URL}/register/", json=payload)
        if response.status_code == 200:
            return True
    except Exception as e:
        pass
    return False

def subscribe_notifications(email, sport, location):
    payload = {"email": email, "sport": sport, "location": location}
    try:
        response = requests.post(f"{BACKEND_URL}/subscribe/", json=payload)
        return response.status_code == 200
    except:
        return False

def fetch_registrations(tournament_id):
    try:
        response = requests.get(f"{BACKEND_URL}/tournaments/{tournament_id}/registrations")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

# --- Sidebar Navigation ---
st.sidebar.image("https://img.icons8.com/color/96/000000/trophy.png", width=60)
st.sidebar.title("Sport Connect 🏆")
page = st.sidebar.radio("Navigation", ["🔍 Discover", "🏗️ Organizer Dashboard", "🤖 AI Assistant"])

st.sidebar.markdown("---")
st.sidebar.info("Connecting players with local tournaments. Bridge the gap between talent and opportunity.")

if page == "🔍 Discover":
    st.title("Discover Local Tournaments")
    st.markdown("Find the best sports tournaments happening near you.")
    
    col1, col2 = st.columns(2)
    with col1:
        search_sport = st.text_input("Filter by Sport (e.g., Cricket, Football)", placeholder="Enter sport...")
    with col2:
        search_location = st.text_input("Filter by Location", placeholder="Enter city or area...")
        
    with st.expander("🔔 Subscribe to new tournament alerts"):
        with st.form("subscribe_form", clear_on_submit=True):
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            with sub_col1:
                sub_email = st.text_input("Email Address")
            with sub_col2:
                sub_sport = st.text_input("Sport (Optional)")
            with sub_col3:
                sub_location = st.text_input("Location (Optional)")
            submit_sub = st.form_submit_button("Get Alerts")
            if submit_sub:
                if sub_email:
                    if subscribe_notifications(sub_email, sub_sport, sub_location):
                        st.success("Subscribed successfully! You'll be notified when new tournaments match your criteria.")
                    else:
                        st.error("Failed to subscribe.")
                else:
                    st.warning("Email is required to subscribe.")

    st.markdown("---")
    
    tournaments = fetch_tournaments(search_sport, search_location)
    
    if not tournaments:
        st.info("No tournaments found matching your criteria. Try dropping the filters or ask the AI Assistant!")
    else:
        for t in tournaments:
            verified_badge = "✅ <span style='font-size:0.8rem; color:#4ade80;'>Verified</span>" if t.get('is_verified', True) else ""
            with st.container():
                st.markdown(f"""
                <div class="tournament-card">
                    <span class="sport-tag">{t.get('sport').upper()}</span>
                    <h3 style="margin-top:10px;">{t.get('title')}</h3>
                    <p class="location-text">📍 {t.get('location')} | 📅 {t.get('tournament_date')}</p>
                    <p><b>Entry Fee:</b> ₹{t.get('entry_fee')} | <span class="prize-tag"><b>Prize Pool:</b> {t.get('prize_pool')}</span></p>
                    <p><b>Organizer:</b> {t.get('organizer_name')} {verified_badge} 📞 {t.get('contact_details')}</p>
                    <p style="color: #cbd5e1; font-size: 0.9rem;">{t.get('description')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"Register for {t.get('title')}"):
                    with st.form(key=f"reg_form_{t.get('id')}"):
                        p_name = st.text_input("Your Name")
                        p_email = st.text_input("Your Email")
                        t_name = st.text_input("Team Name (Optional)")
                        submit_reg = st.form_submit_button("Submit Registration")
                        
                        if submit_reg:
                            if p_name and p_email:
                                success = register_player(t.get('id'), p_name, p_email, t_name)
                                if success:
                                    st.success("Successfully registered! The organizer will contact you soon.")
                                else:
                                    st.error("Registration failed. Please try again.")
                            else:
                                st.warning("Name and Email are required!")

elif page == "🏗️ Organizer Dashboard":
    st.title("Organizer Dashboard")
    st.markdown("Host a tournament and manage players.")
    
    org_tab1, org_tab2 = st.tabs(["🚀 Host a Tournament", "👥 Manage My Tournaments"])
    
    with org_tab1:
        with st.form("create_tournament"):
            st.subheader("Tournament Details")
            t_title = st.text_input("Tournament Title", placeholder="e.g., Summer Smash T20")
            
            col1, col2 = st.columns(2)
            with col1:
                t_sport = st.text_input("Sport", placeholder="e.g., Cricket")
                t_fee = st.number_input("Entry Fee (₹)", min_value=0, value=500)
                t_date = st.date_input("Tournament Date")
            with col2:
                t_location = st.text_input("Location", placeholder="e.g., Central Park Ground, Mumbai")
                t_prize = st.text_input("Prize Pool", placeholder="e.g., ₹50,000 + Trophy")
                t_org = st.text_input("Organizer Name", placeholder="Your Name/Club")
                
            t_contact = st.text_input("Contact Details", placeholder="Phone number or Email")
            t_desc = st.text_area("Description / Rules", placeholder="Any specific rules, timings, etc.")
            
            submit = st.form_submit_button("List Tournament 🚀")
            
            if submit:
                if t_title and t_sport and t_location and t_org:
                    payload = {
                        "title": t_title,
                        "sport": t_sport,
                        "location": t_location,
                        "entry_fee": t_fee,
                        "prize_pool": t_prize,
                        "organizer_name": t_org,
                        "contact_details": t_contact,
                        "tournament_date": t_date.strftime("%Y-%m-%d"),
                        "description": t_desc
                    }
                    try:
                        res = requests.post(f"{BACKEND_URL}/tournaments/", json=payload)
                        if res.status_code == 200:
                            st.success(f"Successfully listed '{t_title}'!")
                        else:
                            st.error("Failed to create. Backend error.")
                    except Exception as e:
                        st.error(f"Could not connect to backend. {e}")
                else:
                    st.warning("Please fill out all mandatory fields (Title, Sport, Location, Organizer).")
                    
    with org_tab2:
        st.subheader("View Registered Players")
        org_search_name = st.text_input("Enter your Organizer Name to view your tournaments")
        if org_search_name:
            all_t = fetch_tournaments()
            org_tournaments = [t for t in all_t if t.get('organizer_name', '').lower() == org_search_name.lower()]
            
            if org_tournaments:
                for target_t in org_tournaments:
                    with st.expander(f"🏅 {target_t.get('title')} - {target_t.get('sport')} ({target_t.get('location')})"):
                        st.write(f"**Date:** {target_t.get('tournament_date')}")
                        registrations = fetch_registrations(target_t.get('id'))
                        if registrations:
                            import pandas as pd
                            df = pd.DataFrame(registrations)
                            st.dataframe(df[['player_name', 'player_email', 'team_name']], use_container_width=True)
                            st.write(f"Total Registrations: **{len(registrations)}**")
                        else:
                            st.info("No players registered yet.")
            else:
                st.warning("No tournaments found for this organizer name.")

elif page == "🤖 AI Assistant":
    st.title("AI Sports Guide")
    st.markdown("Ask me anything! I can find tournaments, compare prizes, or check entry fees for you.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your Sport Connect Assistant. What kind of tournament are you looking for today?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("E.g., Find me cheap cricket tournaments in Mumbai"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/ai/chat", json={"message": prompt})
                    if response.status_code == 200:
                        reply = response.json().get("response", "No response.")
                    else:
                        reply = "Sorry, the AI service returned an error."
                except Exception as e:
                    reply = "Sorry, I can't reach the backend server right now."
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
