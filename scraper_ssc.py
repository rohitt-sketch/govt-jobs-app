# scraper_ssc.py
import requests
from bs4 import BeautifulSoup
import urllib3
from config import USER_AGENT
from db import supabase
from notifier import send_telegram

# Warning ko ignore karne ke liye (kyunki kuch sarkari sites secure nahi hoti)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_ssc():
    url = "https://ssc.gov.in/"
    headers = {"User-Agent": USER_AGENT}
    print(f"🔍 {url} se data laa rahe hain...")

    try:
        # Website se data mangwaya
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Website open nahi hui: {e}")
        return

    # HTML ko parse kiya (padhne layak banaya)
    soup = BeautifulSoup(response.text, "lxml")

    # SSC website par jitne bhi links (a tag) hain, unhe dhoonda
    links = soup.find_all("a", href=True)
    
    new_count = 0
    for a in links:
        title = a.get_text(strip=True)
        href = a.get("href", "")

        # Chote aur bekaar links ko skip karo
        if len(title) < 15: 
            continue
        if not (href.startswith("http") or href.startswith("/")):
            continue

        # Agar link aadha hai (jaise /notice/123), to pura banao
        if href.startswith("/"):
            href = url.rstrip("/") + href

        # Check karo ki ye naukri pehle se database mein hai kya?
        try:
            existing = supabase.table("jobs").select("id").eq("notification_url", href).execute()
            if existing.data:
                continue # Agar pehle se hai to skip karo
        except Exception as e:
            print(f"Database check error: {e}")
            continue

        # Agar naya hai, to database mein save karo
        try:
            supabase.table("jobs").insert({
                "title": title,
                "organization": "SSC",
                "notification_url": href
            }).execute()
            
            # Telegram par message bhejo
            send_telegram(f"🔔 Nayi naukri (SSC)!\n\n{title}\n\nLink: {href}")
            print(f"✅ Saved: {title[:60]}")
            new_count += 1
            
        except Exception as e:
            print(f"❌ Save error: {e}")

    print(f"\n🎉 Total {new_count} nayi jobs mili aur save hui!")

if __name__ == "__main__":
    scrape_ssc()