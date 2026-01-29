import psycopg2

try:
    # Veritabanına bağlan
    conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="hasan123")
    cursor = conn.cursor()

    # 1. Tabloyu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS satislar 
                      (id SERIAL PRIMARY KEY, musteri_id INTEGER, urun_adi TEXT)''')
    
    # 2. İçini temizle (varsa eski veriler gitsin)
    cursor.execute("TRUNCATE TABLE satislar")

    # 3. Örnek Trendyol verilerini ekle
    veriler = [
        (1, 'Utu'), (1, 'Utu Masasi'), (1, 'Kirec Cozucu'),
        (2, 'Utu'), (2, 'Kirec Cozucu'),
        (3, 'Utu Masasi'), (3, 'Camasir Sepeti'),
        (4, 'Utu'), (4, 'Utu Masasi'),
        (5, 'Camasir Makinesi'), (5, 'Deterjan'),
        (6, 'Utu'), (6, 'Utu Masasi'), (6, 'Kirec Cozucu')
    ]
    
    for v in veriler:
        cursor.execute("INSERT INTO satislar (musteri_id, urun_adi) VALUES (%s, %s)", v)

    conn.commit()
    print("Müjde! 'satislar' tablosu oluşturuldu ve veriler yüklendi.")

except Exception as e:
    print(f"Hata: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()