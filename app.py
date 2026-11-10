# app.py
import streamlit as st
from db import supabase

# Page ki setting (Title aur icon)
st.set_page_config(page_title="Sarkari Naukri Alert", page_icon="🇮🇳", layout="wide")

# Custom CSS se website ko sundar banate hain
st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Title styling */
    h1 {
        color: #1f4e78;
        text-align: center;
        font-family: 'Arial', sans-serif;
        padding-bottom: 20px;
    }
    /* Subheader styling */
    h2 {
        color: #2c3e50;
        font-size: 1.5rem !important;
    }
    /* Button styling */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    /* Link Button styling */
    .stLinkButton>a {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        font-weight: bold !important;
    }
    .stLinkButton>a:hover {
        background-color: #218838 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇮🇳 Sarkari Naukri — Latest Updates")
st.write("Yahan aapko sabhi latest sarkari naukriyan ek jagah milengi.")

# Sidebar mein Search Bar
with st.sidebar:
    st.header("🔍 Search Naukri")
    search_query = st.text_input("Naukri ka naam ya department likhein:")
    st.markdown("---")
    st.info("Nayi naukri aane par aapko Telegram par alert milega.")

# Database se saari jobs mangwao
try:
    response = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
    jobs = response.data
except Exception as e:
    st.error(f"Database se data nahi aa raha: {e}")
    jobs = []

st.divider()

if not jobs:
    st.warning("Abhi koi naukri nahi hai. Pehle scraper chalao.")
else:
    # Filter logic (Search)
    if search_query:
        filtered_jobs = [
            job for job in jobs 
            if search_query.lower() in job.get("title", "").lower() or 
               search_query.lower() in job.get("organization", "").lower()
        ]
    else:
        filtered_jobs = jobs

    st.write(f"**Total {len(filtered_jobs)} naukriyan mili hain:**")
    
    # Ek-ek karke saari jobs dikhao
    for job in filtered_jobs:
        with st.container():
            # Ek card jaisa design
            st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;">
                    <h2 style="margin-top: 0; color: #1f4e78;">{job.get('title', 'No Title')}</h2>
                    <p style="font-size: 1.1rem; color: #555;"><b>Organization:</b> {job.get('organization', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Button
            if job.get("notification_url"):
                st.link_button("📄 Notification dekho", job["notification_url"])
            
            st.write("") # Thoda space
