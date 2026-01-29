import requests
import psycopg2

# 1. PostgreSQL'e Bağlantı Ayarları
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="hasan123"  # Buraya terminalde girdiğin şifreyi yaz
    )
    cursor = conn.cursor()

    # 2. Tabloyu Oluşturalım (Eğer yoksa)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_gorevler (
            id SERIAL PRIMARY KEY,
            kullanici_id INTEGER,
            baslik TEXT,
            tamamlandi BOOLEAN
        )
    ''')

    # 3. API'den Verileri Çekelim
    print("Veriler API'den alınıyor...")
    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data = response.json()

    # 4. Verileri Veritabanına Yazalım (İlk 20 tanesini)
    for gorev in data[:20]:
        cursor.execute(
            "INSERT INTO api_gorevler (kullanici_id, baslik, tamamlandi) VALUES (%s, %s, %s)",
            (gorev['userId'], gorev['title'], gorev['completed'])
        )

    # 5. İşlemleri Onayla ve Kapat
    conn.commit()
    print("Müjde! Veriler PostgreSQL veritabanına başarıyla kaydedildi.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()