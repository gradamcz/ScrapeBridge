import requests
from bs4 import BeautifulSoup
import csv

# Add your Waterway Guide bridge URLs here
urls = [
    "https://www.waterwayguide.com/bridge/3-199/boca-grande-swing-bridge", "https://www.waterwayguide.com/bridge/3-200/manasota-key-tom-adams-bridge", "https://www.waterwayguide.com/bridge/3-201/manasota-bridge", "https://www.waterwayguide.com/bridge/3-202/tamiami-trail-circus-bridges-twin", "https://www.waterwayguide.com/bridge/3-203/venice-avenue-bridge", "https://www.waterwayguide.com/bridge/3-204/kmi-hatchett-creek-bridge", "https://www.waterwayguide.com/bridge/3-205/albee-road-casey-key-bridge", "https://www.waterwayguide.com/bridge/3-206/blackburn-point-bridge", "https://www.waterwayguide.com/bridge/3-207/stickney-point-sr-72-bridge", "https://www.waterwayguide.com/bridge/3-208/siesta-drive-bridge", "https://www.waterwayguide.com/bridge/3-209/ringling-causeway-sr-789-bridge", "https://www.waterwayguide.com/bridge/3-211/longboat-pass-sr-789-bridge-to-gulf", "https://www.waterwayguide.com/bridge/3-212/cortez-sr-684-bridge", "https://www.waterwayguide.com/bridge/3-213/anna-maria-island-sr-64-manatee-avenue-west-bridge", "https://www.waterwayguide.com/bridge/3-215/sunshine-skyway-meisner-bridge", "https://www.waterwayguide.com/bridge/3-229/pinellas-bayway-structure-e-sr-679-bridge", "https://www.waterwayguide.com/bridge/3-230/pinellas-bayway-c-bridge", "https://www.waterwayguide.com/bridge/3-231/corey-causeway-sr-693-bridge", "https://www.waterwayguide.com/bridge/3-232/treasure-island-causeway-bridge", "https://www.waterwayguide.com/bridge/3-233/johns-pass-bridge-to-gulf", "https://www.waterwayguide.com/bridge/3-234/welch-causeway-sr-699-bridge", "https://www.waterwayguide.com/bridge/3-235/park-boulevard-sr-248-bridge", "https://www.waterwayguide.com/bridge/3-236/indian-rocks-beach-cr-694-bridge", "https://www.waterwayguide.com/bridge/3-237/belleair-causeway-bridge", "https://www.waterwayguide.com/bridge/3-239/clearwater-memorial-causeway-sr-60-bridge", "https://www.waterwayguide.com/bridge/3-238/clearwater-pass-sr183-bridge-to-gulf", "https://www.waterwayguide.com/bridge/3-240/dunedin-honeymoon-island-bridge", "https://www.waterwayguide.com/bridge/3-192/sr-865-matanzas-pass-bridge", "https://www.waterwayguide.com/bridge/3-194/sanibel-causeway-boulevard-a-span-bridge", "https://www.waterwayguide.com/bridge/3-193/big-carlos-pass-sr-865-bridge", "https://www.waterwayguide.com/bridge/3-197/matlacha-pass-sr-78-bridge", "https://www.waterwayguide.com/bridge/3-188/cape-coral-bridge", "https://www.waterwayguide.com/bridge/3-187/midpoint-memorial-bridge", "https://www.waterwayguide.com/bridge/3-186/us-41caloosahatchee-river-bridge", "https://www.waterwayguide.com/bridge/3-185/edison-bridges", "https://www.waterwayguide.com/bridge/3-184/scl-railroad-bridge", "https://www.waterwayguide.com/bridge/3-183/i-75-bridges", "https://www.waterwayguide.com/bridge//3-182/wilson-pigott-drawbridge", "https://www.waterwayguide.com/bridge/3-180/alva-drawbridge", "https://www.waterwayguide.com/bridge/3-179/fort-denaud-bridge", "https://www.waterwayguide.com/bridge/3-178/la-belle-sr-29-bridge", "https://www.waterwayguide.com/bridge/3-176/moore-haven-us-27-bridges", "https://www.waterwayguide.com/bridge/3-175/seaboard-system-railroad-bridge", "https://www.waterwayguide.com/bridge/3-173/torry-island-cr-717-bridge", "https://www.waterwayguide.com/bridge/3-171/us-98441-bridge", "https://www.waterwayguide.com/bridge/3-170/florida-east-coast-railroad-bridge", "https://www.waterwayguide.com/bridge/3-169/seaboard-system-railroad-bridge", "https://www.waterwayguide.com/bridge/3-114/indiantown-sr-710-bridge", "https://www.waterwayguide.com/bridge/3-167/sr-76a-bridge", "https://www.waterwayguide.com/bridge/3-165/florida-turnpike-bridges", "https://www.waterwayguide.com/bridge/3-164/i-95-twin-bridges", "https://www.waterwayguide.com/bridge/3-534/southwest-martin-highway-bridge", "https://www.waterwayguide.com/bridge/3-163/palm-city-sr-714-bridge", "https://www.waterwayguide.com/bridge/3-162/old-roosevelt-dixie-highway-bridge", "https://www.waterwayguide.com/bridge/3-161/florida-east-coast-railroad-bridge-stuart", "https://www.waterwayguide.com/bridge/3-160/roosevelt-us-1-bridge", "https://www.waterwayguide.com/bridge/3-159/evans-crary-sr-a1a-bridge"
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
