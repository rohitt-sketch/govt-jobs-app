# app.py
import streamlit as st
from db import supabase

# Page Configuration
st.set_page_config(page_title="Sarkari Naukri Alert", page_icon="🇮🇳", layout="wide")

# Custom CSS (Website ko sundar banane ke liye)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Top Banner */
    .header-banner {
        background: linear-gradient(135deg, #1f4e78, #3498db);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .header-banner p {
        font-size: 1.1rem;
        margin-top: 10px;
        opacity: 0.9;
    }
    /* Job Card Design */
    .job-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 5px solid #3498db;
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .job-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .job-org {
        display: inline-block;
        background-color: #e1f5fe;
        color: #0277bd;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    /* Button Design */
    .stLinkButton > a {
        background-color: #27ae60 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        font-weight: bold !important;
        display: inline-block;
        transition: background-color 0.3s;
    }
    .stLinkButton > a:hover {
        background-color: #219653 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div class="header-banner">
        <h1>🇮🇳 Sarkari Naukri Alert</h1>
        <p>Aapki sabhi latest government jobs ek hi jagah</p>
    </div>
""", unsafe_allow_html=True)

# Search Bar (Sidebar mein)
with st.sidebar:
    st.markdown("### 🔍 Search Naukri")
    search_query = st.text_input("", placeholder="Naukri ka naam likhein...")
    st.markdown("---")
    st.success("🔔 Nayi naukri aane par Telegram par alert milega!")

# Data Fetch
try:
    response = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
    jobs = response.data
except Exception as e:
    st.error(f"Database Error: {e}")
    jobs = []

# Filter Logic
if search_query:
    filtered_jobs = [
        job for job in jobs 
        if search_query.lower() in job.get("title", "").lower() or 
           search_query.lower() in job.get("organization", "").lower()
    ]
else:
    filtered_jobs = jobs

# Display Count
if not filtered_jobs:
    st.info("Abhi koi naukri nahi mili. Kripya scraper chalao.")
else:
    st.markdown(f"### Aapke liye **{len(filtered_jobs)}** naukriyan mili hain:")
    st.write("---")

    # Display Cards
    for job in filtered_jobs:
        st.markdown(f"""
            <div class="job-card">
                <div class="job-org">{job.get('organization', 'Govt')}</div>
                <div class="job-title">{job.get('title', 'No Title')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if job.get("notification_url"):
            # Link button ke liye thoda spacing
            st.link_button("📄 Notification Dekhein", job["notification_url"])
            st.write("") # Space
