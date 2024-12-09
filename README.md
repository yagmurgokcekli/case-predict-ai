# case-predict-ai / veri çekme
### `veriCekme.py`
- **Amaç**: Danıştay kararları veritabanından dava metadatasını çekerek bir CSV dosyasına kaydetmek.
- **Kullanım**: 
  - `POST` isteğiyle belirli kriterlere uyan davaların verileri alınır.
  - Çekilen veri, şu alanları içerecek şekilde `veriler.csv` dosyasına yazılır:
    - `id`: Dava ID'si.
    - `daireKurul`: Daire/Kurul bilgisi.
    - `esasNo`: Esas numarası.
    - `kararNo`: Karar numarası.
    - `kararTarihi`: Karar tarihi.
- **Çalışma Prensibi**:
  - Her sayfada 100 dava verisi çekilir, 51 sayfa boyunca tüm veriler döngü ile işlenir.
  - Çekilen veri, `csv.DictWriter` kullanılarak `veriler.csv` dosyasına eklenir.
 
 ### `belgeCekme.py`
- **Amaç**: `veriler.csv` dosyasından alınan dava ID'leri kullanılarak karar metinlerini çekmek ve işlemek.
- **Kullanım**:
  - Her ID için ayrı bir `GET` isteği yapılır ve dava metni alınır.
  - Metin, HTML içeriklerinden arındırılarak temizlenir.
  - Çekilen veriler şu alanlarla `belgeler.csv` dosyasına yazılır:
    - `id`: Dava ID'si.
    - `belge`: Karar metni (HTML etiketlerinden arındırılmış sade metin).
- **Çalışma Prensibi**:
  - Veriler `BeautifulSoup` kütüphanesi kullanılarak işlenir.
  - Her istek arasında 1 saniyelik bekleme süresi eklenmiştir (`time.sleep(1)`) isteklere karşı limitlenmemek için.
