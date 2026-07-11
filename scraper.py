import requests
from bs4 import BeautifulSoup
import csv

# Add your Waterway Guide bridge URLs here
urls = [
    "https://www.waterwayguide.com/bridge/3-201/manasota-beach-road-bridge"
]

fields = ["Bridge Name", "Mile Marker", "Lat / Lon", "Bridge Type", "Vertical Clearance (Closed)", "Horizontal Clearance", "Schedule"]

with open("bridge_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            if response.status_code != 200:
                print(f"Failed to load {url} (Status: {response.status_code})")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            bridge_info = {f: "N/A" for f in fields}
            
            # 1. Grab Bridge Name precisely from the main page title
            if soup.find('h1'):
                name = soup.find('h1').text.strip()
            elif soup.title:
                name = soup.title.text.split('|')[0].strip() # Cleans up "Title | Waterway Guide" strings
            else:
                name = "Unknown Bridge"
            
            # Clean up potential extra wording from title tags
            bridge_info["Bridge Name"] = name.replace("Bridge Details:", "").replace("Bridge", "").strip() + " Bridge"
            
            # 2. Extract layout fields
            for element in soup.find_all(['li', 'div', 'p']):
                text = " ".join(element.text.split())
                
                if "Mile Marker" in text and ":" in text:
                    bridge_info["Mile Marker"] = text.split(":", 1)[1].strip()
                elif "Lat / Lon" in text and ":" in text:
                    bridge_info["Lat / Lon"] = text.split(":", 1)[1].strip()
                elif "Bridge Type" in text and ":" in text:
                    bridge_info["Bridge Type"] = text.split(":", 1)[1].strip()
                elif "Vertical Clearance" in text and ":" in text:
                    bridge_info["Vertical Clearance (Closed)"] = text.split(":", 1)[1].strip()
                elif "Horizontal Clearance" in text and ":" in text:
                    bridge_info["Horizontal Clearance"] = text.split(":", 1)[1].strip()
                elif "Schedule" in text and ":" in text:
                    bridge_info["Schedule"] = text.split(":", 1)[1].strip()

            # 3. Clean up the Schedule field
            editors_note = "Editor's Note: Bridge schedules are subject to temporary change due to repairs, maintenance, events, etc. Check the Waterway Explorer for possible nav alerts."
            if bridge_info["Schedule"] != "N/A":
                bridge_info["Schedule"] = bridge_info["Schedule"].replace(editors_note, "").strip()

            writer.writerow(bridge_info)
            print(f"Successfully processed: {bridge_info['Bridge Name']}")
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("Scraping finished!")
