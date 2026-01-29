-- Mevcut tabloyu temizleyip daha gerçekçi veriler ekleyelim
TRUNCATE TABLE satislar;

INSERT INTO satislar (musteri_id, urun_adi) VALUES 
(1, 'Utu'), (1, 'Utu Masasi'), (1, 'Kirec Cozucu'),
(2, 'Utu'), (2, 'Kirec Cozucu'),
(3, 'Utu Masasi'), (3, 'Camasir Sepeti'),
(4, 'Utu'), (4, 'Utu Masasi'),
(5, 'Camasir Makinesi'), (5, 'Deterjan'),
(6, 'Utu'), (6, 'Utu Masasi'), (6, 'Kirec Cozucu');