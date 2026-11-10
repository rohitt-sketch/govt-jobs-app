# db.py
import streamlit as st
from supabase import create_client

# Streamlit ki secrets se keys uthao
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    try:
        result = supabase.table("jobs").select("*").execute()
        print("✅ Database se connection ban gaya!")
    except Exception as e:
        print(f"❌ Error: {e}")