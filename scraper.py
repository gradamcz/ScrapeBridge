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
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                print(f"Failed to load {url} (Status: {response.status_code})")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            bridge_info = {f: "N/A" for f in fields}
            
            # 1. Grab Bridge Name
            name_tag = soup.find('h2')
            bridge_info["Bridge Name"] = name_tag.text.strip() if name_tag else "Unknown Bridge"
            
            # 2. Grab all list items and text blocks
            # Look for spans or standard text labels across the page
            page_text = soup.get_text(separator=" ").splitlines()
            
            for line in page_text:
                clean_line = " ".join(line.split())
                
                # Check for each data field anywhere in the line
                for field in fields:
                    if field in clean_line and ":" in clean_line:
                        try:
                            value = clean_line.split(":", 1)[1].strip()
                            if value: # Make sure it's not empty
                                bridge_info[field] = value
                        except IndexError:
                            pass
            
            writer.writerow(bridge_info)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("Scraping finished!")
