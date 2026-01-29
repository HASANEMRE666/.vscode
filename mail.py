import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def mail_gonder():
    # --- AYARLAR ---
    gonderen_mail = "hassemre33@gmail.com"
    # Buraya 1. adımda aldığın 16 haneli Uygulama Şifresini yaz (Boşluksuz)
    uygulama_sifresi = " ptkq ffoy jgbl erzo"
    alici_mail = "hasanemregucum@gmail.com"
    dosya_adi = "gorev_raporu.xlsx"

    # 1. Mesaj Yapısı
    mesaj = MIMEMultipart()
    mesaj["From"] = gonderen_mail
    mesaj["To"] = alici_mail
    mesaj["Subject"] = "Python ile Otomatik Gönderilen Rapor"

    icerik = "Merhaba Hasan Emre, bugün işlenen veriler ekteki Excel dosyasındadır."
    mesaj.attach(MIMEText(icerik, "plain"))

    # 2. Dosya Ekleme (Attachment)
    try:
        with open(dosya_adi, "rb") as dosya:
            ek = MIMEBase("application", "octet-stream")
            ek.set_payload(dosya.read())
        
        encoders.encode_base64(ek)
        ek.add_header("Content-Disposition", f"attachment; filename={dosya_adi}")
        mesaj.attach(ek)

        # 3. Sunucuya Bağlanma ve Gönderme
        print("Mail sunucusuna bağlanılıyor...")
        sunucu = smtplib.SMTP("smtp.gmail.com", 587)
        sunucu.starttls() # Güvenli bağlantı kur
        
        sunucu.login(gonderen_mail, uygulama_sifresi) # Giriş yap
        
        sunucu.sendmail(gonderen_mail, alici_mail, mesaj.as_string())
        sunucu.quit()
        
        print(f"Başarılı! Mail '{alici_mail}' adresine gönderildi.")

    except FileNotFoundError:
        print(f"Hata: '{dosya_adi}' dosyası bulunamadı! Önce Excel'i oluşturmalısın.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    mail_gonder()