from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Veri modelini tanımlıyoruz (Pydantic sayesinde otomatik doğrulama)
class Kitap(BaseModel):
    id: int
    isim: str
    yazar: str
    sayfa_sayisi: int
    ozet: Optional[str] = None # Bu alan opsiyoneldir

# Geçici veri tabanı (Hafızada tutulur)
kitaplar = []

# GET: Tüm kitapları listele
@app.get("/kitaplar")
def kitaplari_getir():
    return kitaplar

# POST: Yeni bir kitap ekle
@app.post("/kitap-ekle")
def kitap_ekle(yeni_kitap: Kitap):
    kitaplar.append(yeni_kitap)
    return {"mesaj": f"'{yeni_kitap.isim}' başarıyla eklendi!"}