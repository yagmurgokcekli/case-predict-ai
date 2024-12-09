import requests
import csv

# dava verilerinin çekileceği url
url = "https://karararama.danistay.gov.tr/aramalist"
headers = {
    "Content-Type": "application/json",  
}

csv_file = "veriler.csv" # çekilen verilerin kaydedileceği csv
fieldnames = ["id", "daireKurul", "esasNo", "kararNo", "kararTarihi"]


try:
    # verilerin kaydedileceği dosyayı bir kere aç
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader() # başlık satırı

    # '2024/' kelimesini içeren 5100 küsür dava olduğundan for 51 kere dönüyor, pageSize = 100
    for i in range(1,52):
        body = {
        "data":{"andKelimeler":["\"2024/\""],"orKelimeler":[],"notAndKelimeler":[],"notOrKelimeler":[],"pageSize":100,"pageNumber":i}
        }

        # POST isteği gönder
        response = requests.post(url, headers=headers, json=body)   
        
        # csv dosyasını append moduyla aç, verileri ekle
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
        
            # requestten dönen verileri csvye yaz
            for row in response.json()["data"]["data"]:
                writer.writerow({
                    "id": row["id"],
                    "daireKurul": row["daireKurul"],
                    "esasNo": row["esasNo"],
                    "kararNo": row["kararNo"],
                    "kararTarihi": row["kararTarihi"],
                })
   
except requests.exceptions.RequestException as e:
    print(f"Bir hata oluştu: {e}")