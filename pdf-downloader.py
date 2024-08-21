import os
import requests
import bs4
from urllib.parse import urljoin

if not os.path.exists("pdfs"):
    os.makedirs("pdfs")

main_url = "https://pastpapers.co/cie/?dir=A-Level/Biology-9700"

response = requests.get(main_url)
soup = bs4.BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

for link in links:
    subpage_text = link.text.strip()
    if 'March' in subpage_text or 'May' in subpage_text:
        subpage_url = urljoin(main_url, link.get('href'))
        print(f"Accessing subpage: {subpage_url}")

        response2 = requests.get(subpage_url)
        soup2 = bs4.BeautifulSoup(response2.text, "html.parser")

        links2 = soup2.find_all("a")
        for link2 in links2:
            href = link2.get("href")
            if href and href.endswith(".pdf"):
                pdf_name = href.split("/")[-1]
                if 'qp' in pdf_name or 'ms' in pdf_name: 
                    pdf_url = urljoin(subpage_url, href)
                    print(f"Downloading PDF: {pdf_name} from {pdf_url}")
                    
                    pdf_path = os.path.join("pdfs", pdf_name)
                    pdf_response = requests.get(pdf_url)
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_name} to {pdf_path}")
