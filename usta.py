import streamlit as st
import math

st.set_page_config(page_title="Usta İşi Tesisat Hesaplayıcı", layout="centered", page_icon="🔧")

st.title("🔧 Detaylı Saha Teklif Aracı")
st.markdown("Tam metraj boru hesabı ve kalem kalem detaylandırılmış aksesuar listesiyle şeffaf müşteri teklifleri oluşturun.")

# --- 1. PROJE VE SEÇİMLER ---
st.subheader("📋 Proje Alanı")
alan = st.number_input("Döşenecek Net Alan (m²):", min_value=10, value=100, step=5)
kat_sayisi = st.selectbox("Kat/Bölge Sayısı (Kollektör Adedi):", [1, 2, 3, 4])

st.subheader("🛠️ Malzeme Seçimi ve Kâr")
col1, col2 = st.columns(2)
with col1:
    boru_secim = st.selectbox("Boru Tipi (Metre Fiyatlı):", [
        "Frankische PE-RT (25.00 TL/m)", 
        "Frankische PEX-A (35.00 TL/m)", 
        "Kalde PE-RT (18.00 TL/m)"
    ])
    kollektor_secim = st.selectbox("TDS Kollektör Tipi:", [
        "Kendinden Vanalı (510.00 TL/Ağız)", 
        "Debi Ayarlı (850.00 TL/Ağız)"
    ])

with col2:
    strafor_secim = st.selectbox("Karplus Yalıtım Straforu:", [
        "26 DNS (121.50 TL/m²)", 
        "30 DNS (148.80 TL/m²)"
    ])
    kar_marji = st.slider("İşçilik + Kâr Marjı Ekle (%):", min_value=0, max_value=100, value=30, step=5)

# --- 2. HESAPLAMA MOTORU ---
if st.button("🧮 Detaylı Teklifi Çıkar", type="primary", use_container_width=True):
    
    # Fiyatları ayıklama
    boru_metre_fiyati = float(boru_secim.split("(")[1].split(" ")[0])
    strafor_fiyati = float(strafor_secim.split("(")[1].split(" ")[0])
    kollektor_agiz_fiyati = float(kollektor_secim.split("(")[1].split(" ")[0])

    # 1. Zemin Grubu (Tam Metraj)
    boru_metraj = alan * 7
    mal_boru = boru_metraj * boru_metre_fiyati
    mal_strafor = alan * strafor_fiyati
    
    zemin_saf_maliyet = mal_boru + mal_strafor
    zemin_satis = zemin_saf_maliyet * (1 + (kar_marji / 100))
    birim_m2_satis = zemin_satis / alan

    # 2. Aksesuar ve Merkezi Sistem Grubu
    toplam_agiz = math.ceil(boru_metraj / 75)
    agiz_per_kat = math.ceil(toplam_agiz / kat_sayisi) # Her kata düşen ağız sayısı
    
    # Kollektör dolabı boyutu kararı (6 ağza kadar 60cm, üstü 80cm)
    dolap_tipi = "60CM Ekolüks" if agiz_per_kat <= 6 else "80CM Ekolüks"
    dolap_birim_fiyat = 1150.00 if agiz_per_kat <= 6 else 2000.00

    rekor_sayisi = toplam_agiz * 2
    kesme_vana_sayisi = kat_sayisi * 2
    u_klips_sayisi = alan * 25
    
    mal_kollektor = toplam_agiz * kollektor_agiz_fiyati
    mal_rekor = rekor_sayisi * 90.00
    mal_vana = kesme_vana_sayisi * 520.00
    mal_klips = u_klips_sayisi * 0.60
    mal_dolap = kat_sayisi * dolap_birim_fiyat
    
    aksesuar_saf_maliyet = mal_kollektor + mal_rekor + mal_vana + mal_klips + mal_dolap
    aksesuar_satis = aksesuar_saf_maliyet * (1 + (kar_marji / 100))
    
    genel_toplam = zemin_satis + aksesuar_satis

    # --- 3. EKRAN ÇIKTILARI VE TEKLİF DÖKÜMÜ ---
    st.success("✅ Teklif Başarıyla Oluşturuldu!")
    
    st.markdown("### 🗣️ Müşteriye Sunulacak Ana Fiyatlar")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #ffc107;">
            <p style="margin:0; color: #856404; font-size: 14px;">Zemin İşçilik Dahil (Boru+Strafor)</p>
            <h3 style="margin:5px 0 0 0; color: #856404;">{birim_m2_satis:,.0f} TL / m²</h3>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background-color: #e2e3e5; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #6c757d;">
            <p style="margin:0; color: #383d41; font-size: 14px;">Merkezi Dağıtım Sistemi (Kollektör Seti)</p>
            <h3 style="margin:5px 0 0 0; color: #383d41;">+ {aksesuar_satis:,.0f} TL</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<h4 style='text-align: right; color: #28a745;'>Anahtar Teslim Toplam: {genel_toplam:,.0f} TL</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # DETAYLI MALZEME LİSTESİ (KÂR EKLENMİŞ MÜŞTERİ FİYATLARIYLA)
    st.subheader("📝 Müşteriye Verilecek Detaylı Malzeme Listesi")
    st.caption("Aşağıdaki listedeki birim ve toplam fiyatlara belirttiğiniz %{} kâr/işçilik marjı dahildir.".format(kar_marji))
    
    # Çarpan hesaplama (Birim fiyata kârı yedirme)
    kar_carpani = 1 + (kar_marji / 100)
    
    st.code(f"""
AÇIKLAMA                                         MİKTAR       TOPLAM TUTAR
---------------------------------------------------------------------------
1. ZEMİN YALITIM VE BORULAMA GRUBU
- {boru_secim.split(" (")[0]}                           {int(boru_metraj)} Metre      {mal_boru * kar_carpani:,.2f} TL
- {strafor_secim.split(" (")[0]}                      {alan} m²         {mal_strafor * kar_carpani:,.2f} TL

2. MERKEZİ DAĞITIM VE BAĞLANTI GRUBU
- {agiz_per_kat} Ağızlı {kollektor_secim.split(" (")[0]} Kollektör Seti      {kat_sayisi} Takım        {mal_kollektor * kar_carpani:,.2f} TL
- {dolap_tipi} Kollektör Dolabı                 {kat_sayisi} Adet         {mal_dolap * kar_carpani:,.2f} TL
- TDS Tesisat Kesme Vanası (Gidiş-Dönüş)         {kesme_vana_sayisi} Adet         {mal_vana * kar_carpani:,.2f} TL
- 16x2 Pex/Pe-rt Boru Bağlantı Rekoru            {rekor_sayisi} Adet         {mal_rekor * kar_carpani:,.2f} TL
- Yerden Isıtma U-Klips (Zımba)                  {int(u_klips_sayisi)} Adet        {mal_klips * kar_carpani:,.2f} TL
---------------------------------------------------------------------------
                                         GENEL TOPLAM :       {genel_toplam:,.2f} TL
    """, language="text")
    
    # Ustanın arka plan kontrolü
    st.info(f"🔒 **Usta Gizli Paneli:** Bu projenin size olan net malzeme gelişi **{zemin_saf_maliyet + aksesuar_saf_maliyet:,.0f} TL**'dir. Müşteriye verilen fiyat üzerinden kalan işçilik/kâr payınız **{genel_toplam - (zemin_saf_maliyet + aksesuar_saf_maliyet):,.0f} TL**'dir.")
