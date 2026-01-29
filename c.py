import pandas as pd
import json

# 1. JSON dosyamızı oku
with open("islenmiş_veriler.json", "r", encoding="utf-8") as dosya:
    veri = json.load(dosya)

# 2. Veriyi Pandas DataFrame'e (Tablo yapısına) dönüştür
df = pd.DataFrame(veri)

# 3. Veriyi Excel dosyası olarak kaydet
# index=False diyoruz ki satır numaraları Excel'de gereksiz kalabalık yapmasın
df.to_excel("gorev_raporu.xlsx", index=False)

print("Excel dosyası başarıyla oluşturuldu: gorev_raporu.xlsx")