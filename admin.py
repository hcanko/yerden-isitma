import streamlit as st
import math

st.set_page_config(page_title="Saha Yönetici Paneli", layout="wide", page_icon="⚙️")

st.title("⚙️ İç Kullanım: Detaylı Metraj ve Kapasite Analizi")
st.markdown("Müşteri taleplerine anında teknik yanıt vermek için hızlı hesaplama aracı.")

# --- 1. MÜŞTERİDEN ALINAN TEKNİK VERİLER ---
st.header("1. Proje Verileri")
col1, col2, col3 = st.columns(3)

with col1:
    alan_taban = st.number_input("Taban Oturum Alanı (m²):", min_value=20, value=150, step=5)
    kat_sayisi = st.selectbox("Kat Sayısı:", [1, 2, 3, 4])
    hmax = st.number_input("Tavan Yüksekliği (m):", min_value=2.0, max_value=6.0, value=2.8, step=0.1)

with col2:
    sekil = st.selectbox("Evin Şekli:", ["Küp/Kare (Kompakt)", "Dikdörtgen (Standart)", "L-Tipi (Yayvan)"])
    
    # YENİ NESİL TUĞLA SEÇENEKLERİ EKLENDİ
    tugla_tipi = st.selectbox("Dış Duvar (Tuğla) Tipi:", [
        "Taşyünü Dolgulu Akıllı Tuğla (Maks. Yalıtım)",
        "Termotuğla / İzotuğla (Mükemmel Yalıtım)",
        "Gazbeton / Ytong (Çok İyi Yalıtım)", 
        "Bims Blok (İyi Yalıtım)", 
        "Standart Kırmızı Tuğla (Zayıf Yalıtım)"
    ])
    
    cam_tipi = st.selectbox("Pencere Tipi:", ["Standart Çift Cam", "Isıcam Sinerji/Low-E", "Üçlü Cam"])

with col3:
    baki = st.selectbox("Cephe/Güneş:", ["Güney Ağırlıklı (Sıcak)", "Doğu/Batı (Standart)", "Kuzey Ağırlıklı (Soğuk)"])
    ruzgar = st.selectbox("Rüzgar Durumu:", ["Korunaklı", "Açık Alan / Rüzgarlı"])

st.markdown("---")

if st.button("🧮 Mühendislik Reçetesini Çıkar", type="primary", use_container_width=True):
    
    # --- 2. HESAPLAMA MOTORU (ARKA PLAN) ---
    toplam_alan = alan_taban * kat_sayisi
    hacim = toplam_alan * hmax
    baz_kayip = 22 # Ortaca bölgesi için baz değer
    
    # Çarpanlar
    k_sekil = {"Küp/Kare (Kompakt)": 1.0, "Dikdörtgen (Standart)": 1.15, "L-Tipi (Yayvan)": 1.3}[sekil]
    
    # YENİ TUĞLA KATSAYILARI (Termodinamik Değerler)
    k_tugla = {
        "Taşyünü Dolgulu Akıllı Tuğla (Maks. Yalıtım)": 0.70, # %30 Tasarruf
        "Termotuğla / İzotuğla (Mükemmel Yalıtım)": 0.80,     # %20 Tasarruf
        "Gazbeton / Ytong (Çok İyi Yalıtım)": 0.85,          # %15 Tasarruf
        "Bims Blok (İyi Yalıtım)": 0.95,                     # %5 Tasarruf
        "Standart Kırmızı Tuğla (Zayıf Yalıtım)": 1.20       # %20 Ekstra Yük
    }[tugla_tipi]
    
    k_cam = {"Standart Çift Cam": 1.10, "Isıcam Sinerji/Low-E": 0.90, "Üçlü Cam": 0.80}[cam_tipi]
    k_baki = {"Güney Ağırlıklı (Sıcak)": 0.90, "Doğu/Batı (Standart)": 1.0, "Kuzey Ağırlıklı (Soğuk)": 1.15}[baki]
    k_ruzgar = {"Korunaklı": 1.0, "Açık Alan / Rüzgarlı": 1.10}[ruzgar]

    # Isı Pompası Kapasitesi (%15 Boyler ve emniyet payı dahil)
    toplam_watt = hacim * baz_kayip * k_sekil * k_tugla * k_cam * k_baki * k_ruzgar
    kw_hassas = (toplam_watt * 1.15) / 1000
    isipompasi_kw = math.ceil(kw_hassas)
    isipompasi_kw = isipompasi_kw if isipompasi_kw % 2 == 0 else isipompasi_kw + 1

    # Metrajlar (Toplam Alan Üzerinden)
    boru_metraj = toplam_alan * 7
    top_600m_sayisi = math.ceil(boru_metraj / 600)
    
    toplam_agiz = math.ceil(boru_metraj / 75)
    agiz_per_kat = math.ceil(toplam_agiz / kat_sayisi)

    # --- 3. SONUÇ EKRANI (TELEFONDA OKUNACAK KISIM) ---
    st.header(f"2. Çıkan Reçete (Toplam {toplam_alan} m² İçin)")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("⚡ Tavsiye Edilen Isı Pompası", f"{isipompasi_kw} kW", f"Hassas Kayıp: {kw_hassas:.1f} kW")
    c2.metric("📏 Net Boru İhtiyacı", f"{int(boru_metraj)} Metre", f"{top_600m_sayisi} Top (600m) Gider")
    c3.metric("🌀 Kollektör Düzeni", f"{kat_sayisi} Takım", f"Her kata {agiz_per_kat} ağızlı kollektör")

    st.markdown("---")
    
    st.subheader("💬 Müşteriye Söylenecek Hızlı Özet:")
    st.info(f"""
    "Abi senin {alan_taban} metrekare taban oturumlu ({kat_sayisi} katlı, toplam {toplam_alan} m²) evin için gerekli mühendislik hesaplamasını yaptım.
    
    Evinin yalıtım ve cephe durumuna göre;
    - Seni kışın en soğuk günlerde bile üzmeyecek **{isipompasi_kw} kW kapasiteli** bir ısı pompası alman gerekiyor. (Tuğla/Yalıtım seçiminin avantajını cihaza yansıttık.)
    - Yerden ısıtma altyapın için tam **{int(boru_metraj)} metre** Frankische boru döşeyeceğiz. (Bunu tek parça döşeyemeyeceğimiz için siparişe **{top_600m_sayisi} kangal** boru girmemiz lazım).
    - Basıncın düşmemesi ve her odanın eşit ısınması için toplam **{toplam_agiz} ağız kollektöre** ihtiyacımız var. (Bunu da ev {kat_sayisi} katlı olduğu için, her kata **{agiz_per_kat}'lı kollektör seti** koyarak çözeceğiz.)
    - Altına da fire payıyla beraber toplam **{toplam_alan + 5} m² Karplus Strafor** gidecek.
    
    İhtiyacın olan malzeme paketi tam olarak bu şekildedir."
    """)
