import pandas as pd
from sqlalchemy import create_engine

# 1. Veritabanına bağlan
engine = create_engine('postgresql+psycopg2://postgres:hasan123@localhost:5432/postgres')

# ... (bağlantı kısmı aynı) ...

# ... (bağlantı kısmı aynı) ...

def tavsiye_et(urun_adi):
    df = pd.read_sql("SELECT * FROM satislar", engine)
    
    # Adım 1: Ürünü alan BENZERSİZ müşterileri bul
    musteri_listesi = df[df['urun_adi'] == urun_adi]['musteri_id'].unique()
    toplam_musteri_sayisi = len(musteri_listesi)
    
    # Adım 2: Bu müşterilerin aldığı diğer ürünleri bul
    diger_urunler = df[df['musteri_id'].isin(musteri_listesi) & (df['urun_adi'] != urun_adi)]
    
    # Adım 3: Aynı müşterinin aynı ürünü iki kez almış olmasını engelle (Drop Duplicates)
    diger_urunler = diger_urunler.drop_duplicates(subset=['musteri_id', 'urun_adi'])
    
    # Adım 4: Sayım ve Oran
    analiz = diger_urunler['urun_adi'].value_counts().reset_index()
    analiz.columns = ['Onerilen_Urun', 'Adet']
    analiz['Guven_Orani_%'] = (analiz['Adet'] / toplam_musteri_sayisi) * 100
    
    return analiz

print(tavsiye_et('Utu'))