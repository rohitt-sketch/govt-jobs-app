# scraper_csir.py
import requests
from bs4 import BeautifulSoup
from config import USER_AGENT
from db import supabase
from notifier import send_telegram

def scrape_csir():
    # CSIR ki jobs wali website
    url = "https://www.csir.res.in/careers" 
    headers = {"User-Agent": USER_AGENT}
    print(f"🔍 {url} se data laa rahe hain...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Website open nahi hui: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")

    # Website par saare links dhoondo
    links = soup.find_all("a", href=True)
    
    new_count = 0
    for a in links:
        title = a.get_text(strip=True)
        href = a.get("href", "")

        # Sirf un links ko chuno jisme 'career', 'job', 'recruit' ya 'advert' ho
        title_lower = title.lower()
        if not any(word in title_lower for word in ['career', 'job', 'recruit', 'advert', 'vacancy']):
            continue
            
        if len(title) < 10: 
            continue
        if not (href.startswith("http") or href.startswith("/")):
            continue

        if href.startswith("/"):
            href = "https://www.csir.res.in" + href

        # Check karo database mein hai kya
        try:
            existing = supabase.table("jobs").select("id").eq("notification_url", href).execute()
            if existing.data:
                continue 
        except Exception as e:
            continue

        # Naya hai to save karo
        try:
            supabase.table("jobs").insert({
                "title": title,
                "organization": "CSIR",
                "notification_url": href
            }).execute()
            
            send_telegram(f"🔔 Nayi naukri (CSIR)!\n\n{title}\n\nLink: {href}")
            print(f"✅ Saved: {title[:50]}...")
            new_count += 1
            
        except Exception as e:
            pass

    print(f"\n🎉 Total {new_count} nayi jobs mili aur save hui!")

if __name__ == "__main__":
    scrape_csir()