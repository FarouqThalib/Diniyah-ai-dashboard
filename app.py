import streamlit as st
from google import genai

# Konfigurasi Tampilan
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

# Inisialisasi Klien Google Gen AI Online
try:
    client = genai.Client(api_key=api_key.strip())
except Exception as e:
    st.error(f"Gagal menginisialisasi API Key: {e}")
    st.stop()

# Pilihan Model Online
MODEL_NAME = "gemini-3.6-flash"

menu = st.sidebar.radio(
    "Pilih Menu:",
    ["🌐 Terjemah Kitab & Hadits", "📖 Kamus Turats Klasik (Lisanul 'Arab)", "📝 Penyusun Modul Ajar Santri"]
)

# ==========================================
# 1. MENU TERJEMAH ONLINE AKURAT
# ==========================================
if menu == "🌐 Terjemah Kitab & Hadits":
    st.header("🌐 Penerjemah Kitab, Hadits & Bahasa Arab Kontekstual (Online)")
    st.write("Menerjemahkan secara online dengan akurasi tinggi, penyesuaian istilah fikih, dan gramatika nahwu-sharaf.")
    
    col1, col2 = st.columns(2)
    with col1:
        arah = st.selectbox("Arah Terjemahan:", ["Arab ke Indonesia", "Indonesia ke Arab (Fusha Berharakat)"])
        teks_asal = st.text_area("Teks Asal:", height=180, placeholder="Tuliskan ibarat kitab, hadits, atau kalimat di sini...")
        btn_terjemah = st.button("Terjemahkan Online ⚡", type="primary")

    with col2:
        st.write("**Hasil Terjemahan & Ulasan Kontekstual:**")
        if btn_terjemah and teks_asal:
            with st.spinner("AI sedang memproses secara online..."):
                prompt = f"""
                Bertindaklah sebagai pakar bahasa Arab dan ilmu syariat.
                Terjemahkan teks berikut dengan akurasi sangat tinggi.
                Arah terjemahan: {arah}
                Teks: "{teks_asal}"

                Format sajian:
                1. Terjemahan Utama (Lugawi & kontekstual)
                2. Penjelasan Makna Syar'i / Istilah Kunci
                3. Catatan Kaidah / I'rab penting secara ringkas
                """
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=prompt
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Kendala pemanggilan AI Online: {e}")

# ==========================================
# 2. MENU KAMUS TURATS KLASIK ONLINE
# ==========================================
elif menu == "📖 Kamus Turats Klasik (Lisanul 'Arab)":
    st.header("📖 Mu'jam Turats Klasik AI (Pencarian Online)")
    st.caption("Rujukan: Mu'jam Maqayis al-Lughah (Ibnu Faris) & Lisanul 'Arab (Ibnu Manzhur)")
    
    kata_input = st.text_input("Masukkan Kata Arab yang Ingin Dibedah (Akar kata atau bentukan):", placeholder="Contoh: السويق, فقه, رحم, انتهك, صلح")
    btn_bedah = st.button("Bedah Akar Kata Online 🔍", type="primary")
    
    if btn_bedah and kata_input:
        with st.spinner(f"Mencari rujukan Maqayis al-Lughah dan Lisanul 'Arab untuk '{kata_input}' secara online..."):
            prompt_kamus = f"""
            Anda adalah pakar filologi bahasa Arab turats dan mu'jam lughawi.
            Bedah kata Arab berikut secara mendalam: "{kata_input}".
            
            Sajikan dengan format berikut:
            ### 1. Akar Kata & Wazan Asal (أصل الكلمة)
            Sebutkan huruf asal tsulatsi mujarrad dan wazan fi'ilnya.

            ### 2. Poros Makna Maqayis al-Lughah (Ibnu Faris)
            Jelaskan poros makna asal yang diterangkan oleh Ibnu Faris dalam معجم مقاييس اللغة.

            ### 3. Penjelasan Lisanul 'Arab (Ibnu Manzhur)
            Uraikan bagaimana lafaz ini dan derivasinya digunakan dalam lisan bangsa Arab fusha serta syawahidnya jika ada (termasuk penjelasan detail jika kata tersebut merupakan istilah benda/makanan klasik seperti السويق).

            ### 4. Faedah Pengajaran untuk Santri
            Kesimpulan ringkas bagaimana guru menerangkan hakikat makna kata ini agar murid paham kaitan arti bahasa dengan istilah syariat.
            """
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_kamus
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Kendala pemanggilan AI Online: {e}")

# ==========================================
# 3. MENU PENYUSUN MODUL AJAR
# ==========================================
elif menu == "📝 Penyusun Modul Ajar Santri":
    st.header("📝 Penyusun Bahan Ajar Diniyah Otomatis (Online)")
    st.write("Masukkan catatan materi kasar atau ibarat kitab kuning, AI akan merapikannya secara online menjadi 4 bagian siap ajar.")
    
    mapel = st.text_input("Fan Ilmu / Mata Pelajaran:", placeholder="Misal: Fiqih Ibadah, Nahwu, Tarikh")
    judul = st.text_input("Topik / Bab:", placeholder="Misal: Syarat Sah Sholat & Najis Ma'fu")
    catatan = st.text_area("Catatan Mentah Guru (Tempel teks panjang di sini):", height=150)
    btn_susun = st.button("Susun Bahan Ajar Online ⚡", type="primary")
    
    if btn_susun and catatan:
        with st.spinner("AI sedang menganalisis materi secara online..."):
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
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt_modul
                )
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Kendala: {e}")
