import pandas as pd
import psycopg2

# 1. Veriyi SQL'den çek
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="hasan123")
df = pd.read_sql("SELECT * FROM satislar", conn)

# 2. Mekanik Analiz: Hangi ürün hangi ürünle kaç kez beraber satılmış?
def sepet_analizi(hedef_urun):
    # Bu ürünü alanların listesi
    alan_kisiler = df[df['urun_adi'] == hedef_urun]['musteri_id']
    
    # Bu kişilerin aldığı diğer tüm ürünler
    oneriler = df[df['musteri_id'].isin(alan_kisiler) & (df['urun_adi'] != hedef_urun)]
    
    # En çok tekrar edenleri hesapla
    sonuc = oneriler['urun_adi'].value_counts().reset_index()
    sonuc.columns = ['Urun', 'Birlikte Alinma Sayisi']
    
    # Yüzdelik güven oranı ekle (Mekanik Zeka)
    toplam_satis = len(alan_kisiler)
    sonuc['Guven_Orani'] = (sonuc['Birlikte Alinma Sayisi'] / toplam_satis) * 100
    
    return sonuc

# Test: Ütü alan biri için öneriler
print("--- Trendyol Tarzi Oneri Sistemi Sonucu ---")
print(sepet_analizi('Utu'))