# db.py
import os
import streamlit as st
from supabase import create_client

# Check karo ki hum Streamlit par hain ya GitHub Actions par
try:
    # Streamlit ke liye
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    # GitHub Actions ke liye
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    try:
        result = supabase.table("jobs").select("*").execute()
        print("✅ Database se connection ban gaya!")
        print(f"Abhi {len(result.data)} jobs hain.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
