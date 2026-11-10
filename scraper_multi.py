# scraper_multi.py
import os
import requests
from bs4 import BeautifulSoup
from db import supabase
from notifier import send_telegram

USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")

def scrape_site(url, org_name):
    print(f"🔍 {org_name} ({url}) se data laa rahe hain...")
    headers = {"User-Agent": USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ {org_name} open nahi hui: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    links = soup.find_all("a", href=True)
    
    new_count = 0
    for a in links:
        title = a.get_text(strip=True)
        href = a.get("href", "")

        # Sirf un links ko chuno jisme 'recruit', 'career', 'job', 'vacancy' ho
        title_lower = title.lower()
        if not any(word in title_lower for word in ['recruit', 'career', 'job', 'vacancy', 'advert', 'notification']):
            continue
            
        if len(title) < 10: 
            continue
        if not (href.startswith("http") or href.startswith("/")):
            continue

        # Agar aadha link hai to pura banao
        if href.startswith("/"):
            base_url = "/".join(url.split("/")[:3])
            href = base_url + href

        # Database mein check karo
        try:
            existing = supabase.table("jobs").select("id").eq("notification_url", href).execute()
            if existing.data:
                continue 
        except Exception:
            pass

        # Naya hai to save karo
        try:
            supabase.table("jobs").insert({
                "title": title,
                "organization": org_name,
                "notification_url": href
            }).execute()
            
            send_telegram(f"🔔 Nayi naukri ({org_name})!\n\n{title}\n\nLink: {href}")
            print(f"✅ Saved: {title[:50]}...")
            new_count += 1
        except Exception:
            pass

    print(f"🎉 {org_name}: {new_count} nayi jobs mili!")

if __name__ == "__main__":
    # Yahan humne CSTT wala link hata kar UPSC aur CSIR add kiya hai
    scrape_site("https://upsc.gov.in/whats-new", "UPSC")
    scrape_site("https://www.csir.res.in/careers", "CSIR")
