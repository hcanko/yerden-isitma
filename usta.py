import streamlit as st
import math

st.set_page_config(page_title="Usta İşi Tesisat Hesaplayıcı", layout="centered", page_icon="🔧")

st.title("🔧 Usta İşi Saha Teklif Aracı")
st.markdown("Piyasa usulüne uygun şekilde; **m² fiyatını ayrı**, **kollektör/aksesuar setini ayrı** hesaplar.")

# --- 1. USTANIN GİRECEĞİ BİLGİLER ---
st.subheader("📋 Proje Alanı")
alan = st.number_input("Döşenecek Net Alan (m²):", min_value=10, value=100, step=5)
kat_sayisi = st.selectbox("Kat/Bölge Sayısı (Kollektör Adedi):", [1, 2, 3, 4])

st.subheader("🛠️ Malzeme Seçimi ve Kâr")
col1, col2 = st.columns(2)
with col1:
    boru_secim = st.selectbox("Boru Tipi (Top):", [
        "Frankische PE-RT (600m) - 15000 TL", 
        "Frankische PEX-A (600m) - 21000 TL", 
        "Kalde PE-RT (240m) - 4320 TL"
    ])
    kollektor_secim = st.selectbox("TDS Kollektör:", [
        "Kendinden Vanalı (510 TL/Ağız)", 
        "Debi Ayarlı (850 TL/Ağız)"
    ])

with col2:
    strafor_secim = st.selectbox("Karplus Strafor:", [
        "26 DNS (121.5 TL/m²)", 
        "30 DNS (148.8 TL/m²)"
    ])
    # Ustanın kâr marjı
    kar_marji = st.slider("İşçilik + Kâr Marjı Ekle (%):", min_value=0, max_value=100, value=30, step=5)

# --- 2. SAHA USULÜ HESAPLAMA MOTORU ---
if st.button("🧮 Teklifi Çıkar", type="primary", use_container_width=True):
    
    # Fiyatları Ayıklama
    if "600m" in boru_secim:
        kangal_metraj = 600
    else:
        kangal_metraj = 240
        
    boru_top_fiyati = float(boru_secim.split("- ")[1].split(" ")[0])
    strafor_fiyati = float(strafor_secim.split("(")[1].split(" ")[0])
    kollektor_agiz_fiyati = float(kollektor_secim.split("(")[1].split(" ")[0])

    # Metraj ve Adetler 
    teorik_boru_metraj = alan * 7
    top_sayisi = max(1, round(teorik_boru_metraj / kangal_metraj))
    agiz_sayisi = math.ceil(teorik_boru_metraj / 75)
    
    rekor_sayisi = agiz_sayisi * 2
    kesme_vana_sayisi = kat_sayisi * 2
    u_klips_sayisi = alan * 25
    dolap_sayisi = kat_sayisi
    
    # A GRUBU: ZEMİN MALİYETİ (SADECE BORU + STRAFOR)
    mal_boru = top_sayisi * boru_top_fiyati
    mal_strafor = alan * strafor_fiyati
    zemin_saf_maliyet = mal_boru + mal_strafor
    
    # Kârlı Zemin (m2) Satış Fiyatı
    zemin_satis_toplam = zemin_saf_maliyet * (1 + (kar_marji / 100))
    birim_m2_satis_fiyati = zemin_satis_toplam / alan

    # B GRUBU: KOLLEKTÖR VE AKSESUARLAR (M2 HARİCİ)
    mal_kollektor = agiz_sayisi * kollektor_agiz_fiyati
    mal_rekor = rekor_sayisi * 90.00
    mal_vana = kesme_vana_sayisi * 520.00
    mal_klips = u_klips_sayisi * 0.60
    mal_dolap = dolap_sayisi * (1150.00 if (agiz_sayisi / kat_sayisi) <= 6 else 2000.00)
    
    aksesuar_saf_maliyet = mal_kollektor + mal_rekor + mal_vana + mal_klips + mal_dolap
    
    # Kârlı Aksesuar Seti Satış Fiyatı
    aksesuar_satis_toplam = aksesuar_saf_maliyet * (1 + (kar_marji / 100))
    
    genel_toplam = zemin_satis_toplam + aksesuar_satis_toplam

    # --- EKRAN ÇIKTILARI ---
    st.success("✅ Piyasa Usulü Maliyet ve Teklif Hazır!")
    
    # USTANIN GÖRECEĞİ ÖZET
    st.caption(f"🔧 **Usta Geliş (Malzeme Çıkışı):** Zemin Grubu {zemin_saf_maliyet:,.0f} TL + Aksesuar Grubu {aksesuar_saf_maliyet:,.0f} TL")
    
    st.markdown("### 🗣️ Müşteriye Sunulacak Fiyatlar")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ffc107; height: 160px;">
            <p style="margin:0; color: #856404; font-size: 14px;">Zemin İşçilik Dahil (Boru+Strafor)</p>
            <p style="margin:0; color: #856404; font-size: 16px;"><b>METREKARE (m²) FİYATI</b></p>
            <h2 style="margin:10px 0 0 0; color: #856404;">{birim_m2_satis_fiyati:,.0f} TL / m²</h2>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div style="background-color: #e2e3e5; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #6c757d; height: 160px;">
            <p style="margin:0; color: #383d41; font-size: 14px;">Merkezi Sistem (m² Harici)</p>
            <p style="margin:0; color: #383d41; font-size: 16px;"><b>KOLLEKTÖR & AKSESUAR SETİ</b></p>
            <h2 style="margin:10px 0 0 0; color: #383d41;">+ {aksesuar_satis_toplam:,.0f} TL</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**💰 Anahtar Teslim Genel Toplam:** {genel_toplam:,.0f} TL")
    st.info(f"💡 **Müşteriye Söylem Şekli:** \"Abi senin işin metrekaresi **{birim_m2_satis_fiyati:,.0f} TL**'den {zemin_satis_toplam:,.0f} TL tutuyor. Üzerine bir de **{aksesuar_satis_toplam:,.0f} TL** kollektör, dolap, vana ve rekor tesisatı grubumuz var.\"")