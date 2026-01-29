import requests
import psycopg2
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# --- AYARLAR ---
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "hasan123"  # Belirlediğin şifre
}

def proje_calistir():
    conn = None
    try:
        # 1. VERİTABANINA BAĞLAN
        print("Veritabanına bağlanılıyor...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 2. TABLOYU OLUŞTUR VE API'DEN VERİ ÇEK
        cursor.execute('''CREATE TABLE IF NOT EXISTS api_gorevler 
                          (id SERIAL PRIMARY KEY, kullanici_id INTEGER, baslik TEXT, tamamlandi BOOLEAN)''')
        
        print("API'den güncel veriler alınıyor...")
        data = requests.get("https://jsonplaceholder.typicode.com/todos").json()
        
        # Tabloyu temizleyip yeni verileri ekleyelim (tekrar olmasın diye)
        cursor.execute("TRUNCATE TABLE api_gorevler")
        for gorev in data[:30]: # İlk 30 veriyi alalım
            cursor.execute("INSERT INTO api_gorevler (kullanici_id, baslik, tamamlandi) VALUES (%s, %s, %s)",
                           (gorev['userId'], gorev['title'], gorev['completed']))
        conn.commit()

        # 3. İSTATİSTİKLERİ ÇEK VE GRAFİK OLUŞTUR
        cursor.execute("SELECT tamamlandi, COUNT(*) FROM api_gorevler GROUP BY tamamlandi")
        istatistik = dict(cursor.fetchall())
        
        labels = ['Tamamlanan', 'Bekleyen']
        sizes = [istatistik.get(True, 0), istatistik.get(False, 0)]
        
        plt.figure(figsize=(6, 4))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#FF5252'], startangle=140)
        plt.title('Gorevlerin Genel Durumu')
        plt.savefig('grafik.png')
        plt.close()

        # 4. PDF RAPORUNU OLUŞTUR
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(200, 20, txt="VERI ANALIZ RAPORU", ln=True, align='C')
        
        pdf.image('grafik.png', x=50, y=40, w=110)
        pdf.ln(100)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="Yapilacaklar Listesi (Bekleyen Isler):", ln=True)
        pdf.set_font("Arial", size=10)
        
        cursor.execute("SELECT baslik FROM api_gorevler WHERE tamamlandi = False")
        for i, row in enumerate(cursor.fetchall(), 1):
            temiz_metin = f"{i}. {row[0]}".encode('latin-1', 'ignore').decode('latin-1')
            pdf.cell(200, 8, txt=temiz_metin, ln=True)

        pdf.output("Final_Raporu.pdf")
        print("\n" + "="*30)
        print("BÜYÜK BAŞARI!")
        print("1. Veriler API'den çekildi.")
        print("2. PostgreSQL'e kaydedildi.")
        print("3. Analiz yapılıp grafik çizildi.")
        print("4. 'Final_Raporu.pdf' oluşturuldu.")
        print("="*30)

    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    proje_calistir()