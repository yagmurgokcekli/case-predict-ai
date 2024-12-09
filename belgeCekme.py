import requests
import csv
from bs4 import BeautifulSoup
import html
import time

# id'ye göre metin belgesini getiren url
url = "https://karararama.danistay.gov.tr/getDokuman?id="
headers = {
    "Content-Type": "application/json",  
}

input_csv = "veriler.csv" # idlerin çekildiği csv
output_csv = "belgeler.csv" # idlerin belgeleriyle beraber yazıldığı csv

fieldnames = ["id", "belge"]

try:
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  
        next(reader) # headerı atla

        for row in reader:
            try:
                # idleri al ve urle ekle
                updated_url = url + row["id"]
                response = requests.get(updated_url, headers=headers, timeout=10) 
                response.raise_for_status()
                
                if response.status_code == 200:

                    # BeautifulSoup kullanarak metni parse et
                    soup = BeautifulSoup(response.text, "html.parser")

                    # `hiddencontent` idsine sahip paragrafı al
                    hidden_content = soup.find("p", {"id": "hiddencontent"})

                    if hidden_content:
                        # HTML entity'lerini çözmek için tekrar parse et
                        decoded_html = html.unescape(hidden_content.get_text())
                        # BeautifulSoup ile HTML'yi parse et
                        soup2 = BeautifulSoup(decoded_html, 'html.parser')
                        # ilk <p> etiketinin içeriğini al
                        paragraph = soup2.find('p')

                    
                        with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='*') # entityleri * ile böl
                            belge = paragraph.get_text().strip() if paragraph else ""
                            writer.writerow({"id": row["id"], "belge": belge})

            except requests.exceptions.RequestException as e:
                print(f"Request hatası (ID: {row['id']}): {e}")
            except Exception as e:
                print(f"Bir hata oluştu (ID: {row['id']}): {e}")

            time.sleep(1) # request limit yememek için
                        
except FileNotFoundError as e:
    print(f"Dosya bulunamadı: {e}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")



