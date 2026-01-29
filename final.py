import pandas as pd
from sqlalchemy import create_engine
from fpdf import FPDF
import matplotlib.pyplot as plt

# 1. Bağlantı
engine = create_engine('postgresql+psycopg2://postgres:hasan123@localhost:5432/postgres')

def raporu_olustur():
    # VERİLERİ ÇEK
    df_satis = pd.read_sql("SELECT * FROM satislar", engine)
    
    # ANALİZ: Utu için öneriler
    hedef = 'Utu'
    musteriler = df_satis[df_satis['urun_adi'] == hedef]['musteri_id'].unique()
    digerleri = df_satis[df_satis['musteri_id'].isin(musteriler) & (df_satis['urun_adi'] != hedef)]
    digerleri = digerleri.drop_duplicates(subset=['musteri_id', 'urun_adi'])
    analiz = digerleri['urun_adi'].value_counts().reset_index()
    analiz.columns = ['Urun', 'Adet']
    analiz['Oran'] = (analiz['Adet'] / len(musteriler)) * 100

    # PDF OLUŞTUR
    pdf = FPDF()
    pdf.add_page()
    
    # Başlık
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 10, txt="AKILLI TICARET ANALIZ RAPORU", ln=True, align='C')
    pdf.ln(10)

    # Öneri Bölümü
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 204) # Trendyol Mavisi :)
    pdf.cell(200, 10, txt=f"'{hedef}' Alan Musteriler Icin Oneriler:", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    for index, row in analiz.iterrows():
        metin = f"- {row['Urun']}: %{row['Oran']:.0f} birlikte alinma orani"
        pdf.cell(200, 8, txt=metin, ln=True)

    # Grafik Ekleme (Pasta Grafiği)
    plt.figure(figsize=(6,4))
    plt.bar(analiz['Urun'], analiz['Oran'], color=['green', 'blue', 'orange'])
    plt.title(f"{hedef} Satislarina Gore Tamamlayici Urunler")
    plt.ylabel("Guven Orani (%)")
    plt.savefig('oneriler_grafik.png')
    plt.close()

    pdf.ln(10)
    pdf.image('oneriler_grafik.png', x=40, w=130)

    pdf.output("Trendyol_Tarzi_Oneri_Raporu.pdf")
    print("Müthiş! 'Trendyol_Tarzi_Oneri_Raporu.pdf' başarıyla oluşturuldu.")

raporu_olustur()