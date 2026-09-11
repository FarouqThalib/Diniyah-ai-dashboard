import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Guru Diniyah AI",
    page_icon="🕌",
    layout="wide"
)

# Sidebar Konfigurasi API
st.sidebar.title("🕌 Diniyah Smart OS")
api_key = st.sidebar.text_input("Masukkan Google Gemini API Key:", type="password")

if not api_key:
    st.warning("⚠️ Masukkan Gemini API Key Anda di bilah samping (sidebar) untuk mengaktifkan AI Online.")
    st.stop()

# Konfigurasi Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Menu Navigasi
menu = st.sidebar.radio(
    "Pilih Menu:",
    ["🌐 Terjemah Kitab & Hadits", "📖 Kamus Turats Klasik (Lisanul 'Arab)", "📝 Penyusun Modul Ajar Santri"]
)

# ==========================================
# 1. MENU TERJEMAH ONLINE AKURAT
# ==========================================
if menu == "🌐 Terjemah Kitab & Hadits":
    st.header("🌐 Penerjemah Kitab, Hadits & Bahasa Arab Kontekstual")
    st.write("Menerjemahkan nash secara presisi dengan penyesuaian istilah fikih dan gramatika nahwu-sharaf.")
    
    col1, col2 = st.columns(2)
    with col1:
        arah = st.selectbox("Arah Terjemahan:", ["Arab ke Indonesia", "Indonesia ke Arab (Fusha Berharakat)"])
        teks_asal = st.text_area("Teks Asal:", height=180, placeholder="Tuliskan ibarat kitab, hadits, atau kalimat di sini...")
        btn_terjemah = st.button("Terjemahkan Sekarang ⚡", type="primary")

    with col2:
        st.write("**Hasil Terjemahan & Ulasan Kontekstual:**")
        if btn_terjemah and teks_asal:
            with st.spinner("AI sedang menganalisis i'rab dan konteks maknanya..."):
                prompt = f"""
                Bertindaklah sebagai ahli filologi bahasa Arab dan pakar ilmu syariat.
                Terjemahkan teks berikut dengan akurasi sangat tinggi.
                Arah terjemahan: {arah}
                Teks: "{teks_asal}"

                Format output:
                1. Hasil Terjemahan (Lugawi dan kontekstual)
                2. Penjelasan Makna Syar'i / Kaidah Penting (jika teks berupa hadits/ibarat fikih)
                3. Catatan I'rab / Kosakata Kunci yang wajib dipahami penuntut ilmu
                """
                respon = model.generate_content(prompt)
                st.markdown(respon.text)

# ==========================================
# 2. MENU KAMUS TURATS KLASIK
# ==========================================
elif menu == "📖 Kamus Turats Klasik (Lisanul 'Arab)":
    st.header("📖 Mu'jam Turats Klasik AI")
    st.caption("Rujukan: Mu'jam Maqayis al-Lughah (Ibnu Faris) & Lisanul 'Arab (Ibnu Manzhur)")
    
    kata_input = st.text_input("Masukkan Kata Arab yang Ingin Dibedah (Akar kata atau bentukan):", placeholder="Contoh: فقه, رحم, صلح, علم, طهر")
    btn_bedah = st.button("Bedah Akar Kata Sekarang 🔍", type="primary")
    
    if btn_bedah and kata_input:
        with st.spinner(f"Membuka referensi Maqayis al-Lughah dan Lisanul 'Arab untuk '{kata_input}'..."):
            prompt_kamus = f"""
            Anda adalah pakar bahasa Arab klasik dan mu'jam turats.
            Bedah kata Arab berikut: "{kata_input}".
            
            Sajikan dengan format rapi berikut:
            ### 1. Akar Kata & Wazan Asal (أصل الكلمة)
            Sebutkan huruf asal tsulatsi mujarrad dan bab wazan fi'ilnya.

            ### 2. Bedah Makna Maqayis al-Lughah (Ibnu Faris)
            Kutip atau jelaskan apa poros makna asal yang disimpulkan oleh Ibnu Faris dalam kitabnya معجم مقاييس اللغة.

            ### 3. Penjelasan Lisanul 'Arab (Ibnu Manzhur)
            Uraikan bagaimana lafaz ini digunakan dalam lisan fusha, derivasi (pecahan kata) utamanya, serta syawahid (Al-Qur'an/Hadits/Syair) jika ada.

            ### 4. Faedah Pengajaran untuk Santri
            Berikan kesimpulan ringkas bagaimana guru mengajarkan hakikat makna kata ini agar santri paham kaitan arti bahasa dengan istilah syariat.
            """
            respon_kamus = model.generate_content(prompt_kamus)
            st.markdown(respon_kamus.text)

# ==========================================
# 3. MENU PENYUSUN MODUL AJAR
# ==========================================
elif menu == "📝 Penyusun Modul Ajar Santri":
    st.header("📝 Penyusun Bahan Ajar Diniyah Otomatis")
    st.write("Masukkan catatan materi kasar atau ibarat kitab kuning, AI akan merapikannya menjadi 4 bagian siap ajar.")
    
    mapel = st.text_input("Fan Ilmu / Mata Pelajaran:", placeholder="Misal: Fiqih Ibadah, Nahwu, Tarikh")
    judul = st.text_input("Topik / Bab:", placeholder="Misal: Syarat Sah Sholat & Najis Ma'fu")
    catatan = st.text_area("Catatan Mentah Guru (Tempel teks panjang di sini):", height=150)
    btn_susun = st.button("Susun Jadi Bahan Ajar ⚡", type="primary")
    
    if btn_susun and catatan:
        with st.spinner("Menyusun modul siap ajar..."):
            prompt_modul = f"""
            Susunkan bahan ajar untuk santri dari materi mentah berikut:
            Pelajaran: {mapel}
            Bab: {judul}
            Catatan Mentah: "{catatan}"

            Susun ke dalam format:
            1. 💡 **Analogi Sederhana**: Buatkan perumpamaan nyata agar santri cepat paham.
            2. 📖 **Konsep Inti**: Ringkasan padat tanpa kata berbelit.
            3. 🎯 **Poin-Poin Wajib Catat**: 3-5 poin kunci yang harus ditulis santri di buku catatan.
            4. 🗣️ **Pertanyaan Diskusi Kelas**: 1 pertanyaan kritis untuk menguji pemahaman santri.
            """
            respon_modul = model.generate_content(prompt_modul)
            st.markdown(respon_modul.text)
