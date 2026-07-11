import requests
from bs4 import BeautifulSoup
import csv

# Add your Waterway Guide bridge URLs to this list
urls = [
    "https://www.waterwayguide.com/bridge/3-201/manasota-beach-road-bridge"
]

# The headers we want to extract
fields = ["Bridge Name", "Mile Marker", "Lat / Lon", "Bridge Type", "Vertical Clearance (Closed)", "Horizontal Clearance", "Schedule"]

# Open/create a CSV file to write data into
with open("bridge_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    for url in urls:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            bridge_info = {f: "N/A" for f in fields}
            
            # Extract Bridge Name (usually the <h2> tag)
            name_tag = soup.find('h2')
            bridge_info["Bridge Name"] = name_tag.text.strip() if name_tag else "Unknown Bridge"
            
            # Find the specific bullet points on the page
            for li in soup.find_all('li'):
                text = " ".join(li.text.split())
                for field in fields:
                    if text.startswith(field):
                        # Extract everything after the colon
                        bridge_info[field] = text.split(":", 1)[1].strip()
            
            writer.writerow(bridge_info)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("Scraping finished!")
