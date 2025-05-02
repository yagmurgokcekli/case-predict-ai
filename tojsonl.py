import pandas as pd
import json

data = pd.read_csv('cikti.csv')  

#csv dosyası jsonl formatına dönüştürüldü, veri.jsonl dosyasına kaydedildi
with open('veri.jsonl', 'w', encoding='utf-8') as f:
    for index, row in data.iterrows():
        
        record = {
            "input": row['davaMetni'], 
            "output": row['kararMetni'] 
        }
        f.write(json.dumps(record, ensure_ascii=False) + '\n')  
