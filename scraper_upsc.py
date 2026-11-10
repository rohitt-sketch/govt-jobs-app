# scraper_upsc.py
import os
import requests
from bs4 import BeautifulSoup
from db import supabase
from notifier import send_telegram

# GitHub Secrets se USER_AGENT uthao, agar na mile to default use karo
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")

def scrape_upsc():
    # UPSC ki latest updates wali website
    url = "https://upsc.gov.in/whats-new" 
    headers = {"User-Agent": USER_AGENT}
    print(f"🔍 {url} se data laa rahe hain...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Website open nahi hui: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")

    # UPSC ki site par 'whats-new' page mein links tables ke andar hote hain
    links = soup.select("table a, .view-content a, .whats-new-list a")
    
    new_count = 0
    for a in links:
        title = a.get_text(strip=True)
        href = a.get("href", "")

        if len(title) < 10: 
            continue
        if not (href.startswith("http") or href.startswith("/")):
            continue

        # Link ko poora banao
        if href.startswith("/"):
            href = "https://upsc.gov.in" + href

        # Database mein check karo
        try:
            existing = supabase.table("jobs").select("id").eq("notification_url", href).execute()
            if existing.data:
                continue 
        except Exception as e:
            pass

        # Naya hai to save karo
        try:
            supabase.table("jobs").insert({
                "title": title,
                "organization": "UPSC",
                "notification_url": href
            }).execute()
            
            send_telegram(f"🔔 Nayi naukri (UPSC)!\n\n{title}\n\nLink: {href}")
            print(f"✅ Saved: {title[:50]}...")
            new_count += 1
            
        except Exception as e:
            pass

    print(f"\n🎉 Total {new_count} nayi jobs mili aur save hui!")

if __name__ == "__main__":
    scrape_upsc()
