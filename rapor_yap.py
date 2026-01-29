import psycopg2
from fpdf import FPDF
conn = None
# 1. PostgreSQL'e Bağlantı
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="hasan123" # Burayı kendi şifrenle doldur
    )
    cursor = conn.cursor()

    # 2. Verileri Çek
    cursor.execute("SELECT baslik FROM api_gorevler WHERE tamamlandi = False")
    gorevler = cursor.fetchall()

    # 3. PDF Oluştur
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Gunluk Gorev Raporu", ln=True, align='C')
    pdf.ln(10) # Boşluk
    
    pdf.set_font("Arial", size=12)
    for i, gorev in enumerate(gorevler, 1):
        # Türkçe karakter sorunu olmaması için basit harflerle yazdırıyoruz
        temiz_metin = f"{i}. {gorev[0]}".encode('latin-1', 'ignore').decode('latin-1')
        pdf.cell(200, 10, txt=temiz_metin, ln=True)

    # 4. Kaydet
    pdf.output("Gorev_Raporu.pdf")
    print("Müjde! 'Gorev_Raporu.pdf' başarıyla oluşturuldu.")

except Exception as e:
    print(f"Hata oluştu: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()