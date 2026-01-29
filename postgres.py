import psycopg2
import smtplib
from email.message import EmailMessage

# 1. Veritabanından Veri Çekme
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="hasan123")
cursor = conn.cursor()

# Sadece tamamlanmamış (False) görevleri SQL ile sorguluyoruz
cursor.execute("SELECT baslik FROM api_gorevler WHERE tamamlandi = False")
yapilacaklar = cursor.fetchall() 

# Verileri okunabilir bir liste haline getirelim
mesaj_icerigi = "Selam! Bugün bitirmen gereken görevler şunlar:\n\n"
for sira, gorev in enumerate(yapilacaklar, 1):
    mesaj_icerigi += f"{sira}. {gorev[0]}\n"

# 2. Mail Atma Bölümü
mail = EmailMessage()
mail['Subject'] = "Günlük Görev Raporu (PostgreSQL'den)"
mail['From'] = "hassemre33@gmail.com"
mail['To'] = "hasanemregucum@gmail.com"
mail.set_content(mesaj_icerigi)

# Gmail üzerinden gönderim
# Eski kısmı bununla değiştir:
try:
    print("Sunucuya bağlanmaya çalışılıyor (587 portu)...")
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15) # 15 saniye bekle, olmazsa hata ver
    server.starttls() # Güvenli bağlantı moduna geç
    server.login("hassemre33@gmail.com", "oyug btms latx oxdm")
    server.send_message(mail)
    server.quit()
    print("BAŞARILI! Mail kutunu kontrol et.")
except Exception as e:
    print(f"Hata detayı: {e}")

cursor.close()
conn.close()