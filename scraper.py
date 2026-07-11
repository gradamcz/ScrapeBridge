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
            
            # 1. Grab Bridge Name from the main heading
            name_tag = soup.find('h2')
            if not name_tag:
                name_tag = soup.find('h1')
            bridge_info["Bridge Name"] = name_tag.text.strip() if name_tag else "Unknown Bridge"
            
            # 2. Look inside the specific list items (li) or divs on the page
            for element in soup.find_all(['li', 'div', 'p']):
                text = " ".join(element.text.split())
                
                # Check for each field explicitly
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
                    # Capture the text right after the schedule label
                    bridge_info["Schedule"] = text.split(":", 1)[1].strip()

            # Fallback for Schedule if it is in an adjacent element
            if bridge_info["Schedule"] == "N/A" or bridge_info["Schedule"] == "":
                schedule_label = soup.find(text=lambda t: t and "Schedule" in t)
                if schedule_label and schedule_label.parent:
                    next_node = schedule_label.parent.find_next_sibling()
                    if next_node:
                        bridge_info["Schedule"] = next_node.text.strip()

            writer.writerow(bridge_info)
            print(f"Successfully processed: {bridge_info['Bridge Name']}")
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")

print("Scraping finished!")
