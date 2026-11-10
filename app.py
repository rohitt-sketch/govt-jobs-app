# app.py
import streamlit as st
from db import supabase

st.set_page_config(page_title="Sarkari Naukri Alert", page_icon="🇮🇳", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .header-banner {
        background: linear-gradient(135deg, #1f4e78, #3498db);
        padding: 30px; border-radius: 15px; color: white; text-align: center;
        margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-banner h1 { color: white; margin: 0; font-size: 2.5rem; font-weight: 700; }
    .job-card {
        background-color: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 15px;
        border-left: 5px solid #3498db; transition: transform 0.2s;
    }
    .job-title { color: #2c3e50; font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; }
    .job-org {
        display: inline-block; background-color: #e1f5fe; color: #0277bd;
        padding: 5px 12px; border-radius: 20px; font-size: 0.9rem; font-weight: 600; margin-bottom: 15px;
    }
    /* Direct Link Button */
    .stLinkButton > a {
        background-color: #27ae60 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
        font-weight: bold !important;
        display: inline-block;
        width: 100%;
        text-align: center;
        transition: background-color 0.3s;
    }
    .stLinkButton > a:hover {
        background-color: #219653 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-banner">
        <h1>🇮🇳 Sarkari Naukri Alert</h1>
        <p>Latest government jobs ek hi jagah</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔍 Search Naukri")
    search_query = st.text_input("", placeholder="Naukri ya department likhein...")

try:
    response = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
    jobs = response.data
except Exception as e:
    st.error(f"Database Error: {e}")
    jobs = []

if search_query:
    filtered_jobs = [j for j in jobs if search_query.lower() in j.get("title", "").lower() or search_query.lower() in j.get("organization", "").lower()]
else:
    filtered_jobs = jobs

if not filtered_jobs:
    st.info("Abhi koi naukri nahi mili. Kripya scraper chalao.")
else:
    st.markdown(f"### Aapke liye **{len(filtered_jobs)}** naukriyan mili hain:")
    st.write("---")

    for job in filtered_jobs:
        # Job Card
        st.markdown(f"""
            <div class="job-card">
                <div class="job-org">{job.get('organization', 'Govt')}</div>
                <div class="job-title">{job.get('title', 'No Title')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Direct Link Button
        if job.get("notification_url"):
            st.link_button("🌐 Official Website Par Jaayein", job["notification_url"])
        
        st.write("<br>", unsafe_allow_html=True)
