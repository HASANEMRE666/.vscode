import requests
import pandas as pd
import random
from sqlalchemy import create_engine

# 1. API'den Kullanıcı Verilerini Çek (Şehir bilgisi için)
response = requests.get("https://jsonplaceholder.typicode.com/users")
users = response.json()
sehirler = [user['address']['city'] for user in users]

# 2. Mevcut Satış Verilerini Veritabanından Çek
engine = create_engine('postgresql+psycopg2://postgres:hasan123@localhost:5432/postgres')
df_satis = pd.read_sql("SELECT * FROM satislar", engine)

# 3. Rastgele Şehir Ataması Yap (Veriyi zenginleştiriyoruz)
df_satis['sehir'] = [random.choice(sehirler) for _ in range(len(df_satis))]

print("API'den gelen şehirlerle veritabanı zenginleştirildi!")
print(df_satis.head())