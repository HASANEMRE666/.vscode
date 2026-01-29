import logging

# Loglama yapılandırması (Configuration)
logging.basicConfig(
    filename='uygulama.log', # Kaydedilecek dosya adı
    filemode='a',             # 'a' append (ekle), 'w' overwrite (üzerine yaz)
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Kullanıcı giriş yaptı.")
logging.error("Veritabanı bağlantısı başarısız!")

# Farklı seviyelerde log mesajları
logging.debug("Bu bir DEBUG mesajı: Yazılımcı için detaylı teknik bilgi.")
logging.info("Bu bir INFO mesajı: Sistem normal çalışıyor, sadece bilgi veriyorum.")
logging.warning("Bu bir WARNING mesajı: Bir şeyler ters gidebilir, dikkat et!")
logging.error("Bu bir ERROR mesajı: Bir hata oluştu ama program hala çalışıyor.")
logging.critical("Bu bir CRITICAL mesajı: Sistem çöktü veya çok ciddi bir sorun var!")