import streamlit as st
import time

# Sayfa ayarları - Müşteriye şık görünmesi için
st.set_page_config(page_title="Yerden Isıtma Maliyet Hesaplayıcı", layout="centered", page_icon="🔥")
# --- GİZLİLİK VE KURUMSALLIK MODÜLÜ ---
# Sağ üstteki menüyü, GitHub logosunu ve en alttaki Streamlit yazısını gizler.
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1000", use_container_width=True) 
st.title("🔥 Yerden Isıtma Bütçenizi Hesaplayın")
st.markdown("Muğla ve çevresi için **Frankische & TDS** kalitesiyle evinize özel tahmini altyapı maliyetini saniyeler içinde görün.")

# --- MÜŞTERİDEN İSTENECEK BİLGİLER (TABAN OTURUMU MANTIĞI) ---
st.subheader("🏠 Evinizin Bilgileri")
alan_taban = st.number_input("Evinizin taban oturumu yaklaşık kaç metrekare?", min_value=30, max_value=300, value=100, step=10)
kat_secimi = st.radio("Eviniz kaç katlı?", ["Tek Katlı (Daire/Müstakil)", "2 Katlı (Dubleks)", "3 Katlı (Tripleks)"])

# Kat çarpanını belirleme
kat_carpani = 1
if "Dubleks" in kat_secimi:
    kat_carpani = 2
elif "Tripleks" in kat_secimi:
    kat_carpani = 3

# Toplam Alan Hesabı
toplam_alan = alan_taban * kat_carpani

# Arka planda 26 Dens Strafora göre güncellenmiş metrekare birim maliyeti
m2_birim_maliyeti_min = 290 
m2_birim_maliyeti_max = 350

if st.button("🚀 Bütçemi Hesapla", type="primary", use_container_width=True):
    with st.spinner("Evinize özel tesisat ve boru metrajları hesaplanıyor..."):
        time.sleep(1.5)
        
    # Maliyet hesabı (Taban alanı * Kat Sayısı üzerinden)
    min_tutar = toplam_alan * m2_birim_maliyeti_min
    max_tutar = toplam_alan * m2_birim_maliyeti_max
    
    st.success("✅ Hesaplama Tamamlandı!")
    
    # Müşteriye toplam metrekareyi de çaktırmadan gösterelim
    st.caption(f"*(Hesaplama {alan_taban} m² x {kat_carpani} Kat = **Toplam {toplam_alan} m²** net alan üzerinden yapılmıştır.)*")
    
    st.markdown("### 💰 Tahmini Altyapı Malzeme Bütçeniz:")
    st.markdown(f"<h2 style='text-align: center; color: #ff4b4b;'>{min_tutar:,.0f} TL - {max_tutar:,.0f} TL</h2>", unsafe_allow_html=True)
    
    # DİKKAT ÇEKİCİ HARİÇTİR UYARISI 
    st.warning("⚠️ **ÖNEMLİ NOT:** Bu bütçe sadece birinci sınıf Frankische PE-RT borular, TDS Kollektörler ve Karplus 26 Dens Yalıtım malzemelerini (Altyapı sistemini) kapsar. **İşçilik ve Isı Pompası Cihazı fiyatlara HARİÇTİR.**")
    
    # --- RENK DÜZELTMESİ YAPILMIŞ ÖDEME PLANI (PEŞİNAT + TAKSİT) ---
    # Paragraf etiketine 'color: #333333;' ekleyerek yazıyı karanlık modda bile koyu renk yaptık.
    st.markdown("""
    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; border-left: 5px solid #0066cc; margin-top: 15px; margin-bottom: 15px;">
        <h4 style="margin:0; color: #004c99;">💳 Esnek Ödeme Kolaylığı!</h4>
        <p style="margin:5px 0 0 0; font-size: 15px; color: #333333;">Tesisatınızı hemen kurdurun, ödemenizi yorulmadan yapın: Sadece <b style="color: #000000;">%20 Peşinat</b> ve kalanı <b style="color: #000000;">3 Taksit</b> imkanıyla bütçenizi sarsmadan konfora ulaşın.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("👇 Net Fiyat ve Keşif İçin Bize Ulaşın!")
    
    # WHATSAPP BUTONU
    whatsapp_mesaji = f"Merhaba, sitenizden hesaplama yaptım. {alan_taban} m2 taban oturumlu, {kat_secimi} (Toplam {toplam_alan} m2) evim için yerden ısıtma ile ilgili bilgi almak istiyorum. Yüzde 20 peşinat ve 3 taksit kampanyanızdan yararlanmak istiyorum."
    whatsapp_linki = f"https://wa.me/905072784487?text={whatsapp_mesaji}".replace(" ", "%20") # KENDİ NUMARANIZI BURAYA YAZIN
    
    st.markdown(f'<a href="{whatsapp_linki}" target="_blank" style="display: block; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 20px; font-weight: bold;">💬 WhatsApp ile Teklif Al</a>', unsafe_allow_html=True)
