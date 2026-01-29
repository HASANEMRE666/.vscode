import requests
import json

# 1. Canlı veriyi çek
URL = "https://jsonplaceholder.typicode.com/todos"
try:
    response = requests.get(URL)
    response.raise_for_status() # Hata varsa yakala
    tum_gorevler = response.json()
except Exception as e:
    print(f"Hata oluştu: {e}")
    exit()

# 2. VERİYİ İŞLE (Sadece tamamlanmış olanları seç ve başlıklarını büyüt)
islenmis_liste = []

for gorev in tum_gorevler:
    if gorev["completed"] == True:
        yeni_veri = {
            "gorev_id": gorev["id"],
            "baslik": gorev["title"].upper(), # Başlığı büyük harf yap
            "durum": "TAMAMLANDI"
        }
        islenmis_liste.append(yeni_veri)

# 3. İŞLENMİŞ VERİYİ DOSYAYA KAYDET
with open("islenmiş_veriler.json", "w", encoding="utf-8") as dosya:
    json.dump(islenmis_liste, dosya, indent=4, ensure_ascii=False)

print(f"İşlem tamam! {len(islenmis_liste)} adet görev 'islenmiş_veriler.json' dosyasına kaydedildi.")

