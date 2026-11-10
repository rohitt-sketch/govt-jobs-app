# db.py
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

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
    