# app.py
import streamlit as st
from db import supabase

# Page ki setting
st.set_page_config(page_title="Sarkari Naukri Alert", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 Sarkari Naukri — Latest Updates")
st.write("Yahan aapko sabhi latest sarkari naukriyan ek jagah milengi.")

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
    st.write(f"**Total {len(jobs)} naukriyan mili hain:**")
    
    # Ek-ek karke saari jobs dikhao
    for job in jobs:
        with st.container():
            st.subheader(job.get("title", "No Title"))
            st.write(f"**Organization:** {job.get('organization', 'N/A')}")
            
            # Agar link hai to button dikhao
            if job.get("notification_url"):
                st.link_button("📄 Notification dekho", job["notification_url"])
            
            st.divider()