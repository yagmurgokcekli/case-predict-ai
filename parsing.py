import re
import pandas as pd
import csv

def parse_text(text):
    # regex desenleri
    patterns = [
        r"\s*İSTEMİN KONUSU\s*:(.*?)YARGILAMA SÜRECİ",  # 1. Kriter
        r"\s*YARGILAMA SÜRECİ\s*:(.*?)TEMYİZ EDENİN İDDİALARI",  # 2. Kriter
        r"\s*İLGİLİ MEVZUAT\s*:(.*?)HUKUKİ DEĞERLENDİRME",  # 3. Kriter
        r"\s*HUKUKİ DEĞERLENDİRME\s*:(.*?)KARAR SONUCU",  # 4. Kriter
        r"\s*KARAR SONUCU\s*:(.*)"  # 5. Kriter
    ]

    # Sonuçları saklayacak liste
    result = []

    # Her bir deseni kullanarak metnin ilgili kısmını bul
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            result.append(match.group(1).strip())  # Bulunan kısmı listeye ekle
        else:
            result.append(" ")  # Eşleşme bulunmazsa boşluk ekle



    return result


def contains_all_criteria(text):
    # Başlıkların metinde olup olmadığını kontrol et
    criteria = [
        "İLGİLİ MEVZUAT", 
        "HUKUKİ DEĞERLENDİRME", 
        "KARAR SONUCU"
    ]
    
    return all(criterion in text for criterion in criteria)


def clean_text(text):
    # Başlangıç ve sonundaki boşlukları temizle
    cleaned_text = text.strip()
    
    # Fazla boşlukları tek bir boşlukla değiştir
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    # Tüm metni küçük harfe çevir
    return cleaned_text.lower()


# CSV dosyasını oku (sütunlar '*' ile ayrılmış)
df = pd.read_csv('belgeler.csv', delimiter='*', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

# Sonuçları tutmak için bir liste
output_data = []

# Her bir belgeyi işle
for idx, row in df.iterrows():
    text = row['belge']
    
    # Metinde başlıkların tümünün olup olmadığını kontrol et
    if not contains_all_criteria(text):
        continue  # Başlıkların tümü yoksa bu metni atla

    # Parsing işlemi
    parsed_data = parse_text(text)

    # Yeni satır oluştur, metinlerin sırasına göre
    row_data = {'id': row['id']}
    
    # Metin türleri için özel sütun adları
    column_names = [
        'isteminKonusu',      # 1. Kriter
        'yargilamaSüreci',    # 2. Kriter
        'ilgilimevzuat',      # 3. Kriter
        'hukukiDegerlendirme',# 4. Kriter
        'kararSonucu'         # 5. Kriter
    ]
    
    # Her metin türünü ilgili sütuna ekle
    for i, section in enumerate(parsed_data):
        cleaned_section = clean_text(section)  # Metni temizle ve küçük harfe çevir
        row_data[column_names[i]] = cleaned_section

    # Bu satırı listeye ekle
    output_data.append(row_data)

# Yeni DataFrame oluştur
output_df = pd.DataFrame(output_data)

# Sonuçları yeni bir CSV dosyasına kaydet
output_df.to_csv('parsed_belgeler.csv', index=False, encoding='utf-8')