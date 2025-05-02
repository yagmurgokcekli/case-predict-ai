import pandas as pd
import re
import csv

#metinler karar metni ve dava metni olarak ikiye ayrıldı, temizlenip uygun formata getirildi

def parse_text(text):
    # regex desenleri
    patterns = [
        
        r"\.*\s*[\.\.\.\-\*\~\+\=\:\;\#\(\)\[\]\{\}]*\s*İSTEMİN\s+KONUSU\s*:?\s*(.*?)\s*KARAR\s+SONUCU\s*:?\s*(.*)",  # İSTEMİN KONUSU ve KARAR SONUCU arasındaki metin
        r"\s*[\.\.\.\-\*\~\+\=\:\;\#\(\)\[\]\{\}]*\s*KARAR\s+SONUCU\s*:?\s*(.*)"  # KARAR SONUCU sonrasındaki metin
    ]

    result = []

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            result.append(match.group(1).strip()) 
        else:
            result.append(" ")  

    return result


def contains_all_criteria(text):
    
    criteria = [
        r"\s*[\.\.\.\-\*\~\+\=\:\;\#\(\)\[\]\{\}]*\s*İSTEMİN\s+KONUSU\s*", 
        r"\s*[\.\.\.\-\*\~\+\=\:\;\#\(\)\[\]\{\}]*\s*KARAR\s+SONUCU\s*"  
    ]
    
    #başlıkları içrip içermediğini kontrol et
    return all(re.search(pattern, text, re.IGNORECASE) for pattern in criteria)



def clean_text(text):
    #başlangıç ve sonundaki boşlukları temizle
    cleaned_text = text.strip()
    
    #fazla boşlukları tek bir boşlukla değiştir
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    #tüm metni küçük harfe çevir
    return cleaned_text.lower()



#CSV dosyasını oku (sütunlar '*' ile ayrılmış)
df = pd.read_csv('belgeler.csv', delimiter='*', quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

output_data = []


for idx, row in df.iterrows():
    text = row['belge']
    
    if contains_all_criteria(text):
        parsed_data = parse_text(text)

        row_data = {'id': row['id']}
        
        column_names = [
            'davaMetni',      
            'kararMetni'      
        ]
        
        for i, section in enumerate(parsed_data):
            cleaned_section = clean_text(section) 
            row_data[column_names[i]] = cleaned_section

        output_data.append(row_data)

    else:
        print("başlıklar eksik", idx)

   

output_df = pd.DataFrame(output_data)

#sonuçları cikti.csv dosyasına kaydet
output_df.to_csv('cikti.csv', index=False, encoding='utf-8')