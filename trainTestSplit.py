from sklearn.model_selection import train_test_split
import pandas as pd

data = pd.read_json('veri.jsonl', lines=True)

#%80 eğitim, %20 test seti olmak üzere bölündü
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

#bölünen setler ayrı jsonl dosyaları olarak kaydedildi
train_data.to_json('train_data.jsonl', orient='records', lines=True, force_ascii=False)
test_data.to_json('test_data.jsonl', orient='records', lines=True, force_ascii=False)
