import streamlit as st
import pandas as pd
import requests
import random
from sqlalchemy import create_engine, text
from fpdf import FPDF

# 1. Sayfa Ayarları
st.set_page_config(page_title="Trendyol Veri Analiz Merkezi", layout="wide")
st.title("🚀 Uçtan Uca Akıllı Satış & Analiz Paneli")

# 2. API'den Canlı Şehir Verisi Çekme (Hafızada tutar)
@st.cache_data
def sehirleri_getir():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        return [user['address']['city'] for user in response.json()]
    except:
        return ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"]

sehir_havuzu = sehirleri_getir()

# --- VERİTABANI BAĞLANTI BÖLÜMÜ BAŞLANGICI ---
try:
    # Kendi bilgisayarındayken burası çalışacak
    engine = create_engine('postgresql+psycopg2://postgres:hasan123@localhost:5432/postgres')
    df = pd.read_sql("SELECT * FROM satislar", engine)
except Exception as e:
    # İnternetteki (GitHub/Streamlit) site burayı çalıştıracak (Hata vermemesi için)
    st.warning("⚠️ Yerel veritabanı bulunamadı. Şu an örnek verilerle çalışılıyor.")
    data = {
        'satis_id': [1, 2, 3],
        'urun_adi': ['Trendyol Elbise', 'Nike Ayakkabı', 'Samsung Telefon'],
        'miktar': [5, 2, 1],
        'fiyat': [450, 2100, 15000]
    }
    df = pd.DataFrame(data)
# --- VERİTABANI BAĞLANTI BÖLÜMÜ BİTİŞİ ---
    
    # Lokasyonu Müşteri ID ile eşleştir (Canlı veri için dinamik yapı)
    df['sehir'] = df['musteri_id'].apply(lambda x: sehir_havuzu[x % len(sehir_havuzu)])

    # --- SIDEBAR: KONTROL VE VERİ GİRİŞİ ---
    st.sidebar.header("🛠️ İşlem Merkezi")
    
    # Ürün Seçimi
    urunler = sorted(df['urun_adi'].unique())
    hedef_urun = st.sidebar.selectbox("Analiz Edilecek Ana Ürün:", urunler)

    st.sidebar.markdown("---")
    st.sidebar.subheader("➕ Yeni Satış Ekle")
    with st.sidebar.form("yeni_kayit_formu", clear_on_submit=True):
        yeni_id = st.number_input("Müşteri ID", min_value=1, step=1)
        yeni_urun = st.selectbox("Satılan Ürün", ["Utu", "Utu Masasi", "Kirec Cozucu", "Camasir Sepeti", "Deterjan"])
        kaydet = st.form_submit_button("Sisteme İşle")

    if kaydet:
        with engine.connect() as conn:
            sorgu = text("INSERT INTO satislar (musteri_id, urun_adi) VALUES (:m_id, :u_adi)")
            conn.execute(sorgu, {"m_id": yeni_id, "u_adi": yeni_urun})
            conn.commit()
        st.cache_data.clear() # Önemli: Analizi sıfırla ki yeni veriyi görsün
        st.sidebar.success(f"ID:{yeni_id} için {yeni_urun} kaydedildi!")
        st.rerun()

    # --- ANALİZ MOTORU ---
    # Hedef ürünü alan müşterileri bul
    hedef_alan_musteriler = df[df['urun_adi'] == hedef_urun]['musteri_id'].unique()
    
    # Bu müşterilerin aldığı DİĞER ürünleri bul
    diger_urunler = df[df['musteri_id'].isin(hedef_alan_musteriler) & (df['urun_adi'] != hedef_urun)]
    diger_urunler = diger_urunler.drop_duplicates(subset=['musteri_id', 'urun_adi'])
    
    analiz = diger_urunler['urun_adi'].value_counts().reset_index()
    analiz.columns = ['Ürün', 'Adet']
    analiz['Güven Oranı (%)'] = (analiz['Adet'] / len(hedef_alan_musteriler)) * 100

    # --- GÖRSELLEŞTİRME ---
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader(f"🛒 {hedef_urun} Alanların Sepeti")
        st.dataframe(analiz, use_container_width=True)

    with col2:
        st.subheader("📊 Çapraz Satış Başarı Oranı")
        st.bar_chart(data=analiz, x='Ürün', y='Güven Oranı (%)')

    st.divider()
    
    # --- LOKASYON ANALİZİ ---
    st.subheader("📍 Bölgesel Dağılım (Müşteri Lokasyonları)")
    sehir_ozeti = df[df['urun_adi'] == hedef_urun]['sehir'].value_counts()
    st.bar_chart(sehir_ozeti, color="#FF4B4B") # Trendyol kırmızısına yakın bir renk

    # --- PDF RAPORLAMA ---
    def pdf_hazirla():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="STRATEJIK SATIS ANALIZI", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"Urun: {hedef_urun} | Toplam Tekil Musteri: {len(hedef_alan_musteriler)}", ln=True)
        pdf.ln(5)
        for _, r in analiz.iterrows():
            pdf.cell(0, 10, txt=f"- {r['Ürün']}: %{r['Güven Oranı (%)']:.0f} birlikte satis sansi.", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    st.sidebar.markdown("---")
    st.sidebar.download_button("📄 PDF Analiz Raporu İndir", data=pdf_hazirla(), file_name="rapor.pdf")

except Exception as e:
    st.error(f"⚠️ Bağlantı veya Kod Hatası: {e}")