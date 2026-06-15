import streamlit as st
import json
import random

st.set_page_config(
    page_title=" MSDS Mini | Sistem Informasi Bahan Kimia",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def ambil_data():
    with open("database_kimia.json", "r", encoding="utf-8") as berkas:
        return json.load(berkas)

daftar_bahan = ambil_data()

def cari_simbol_ghs(sifat_bahan: str) -> list:
    hasil = []
    sb = sifat_bahan.lower()
    if "korosif" in sb:
        hasil.append("corrosive")
    if "toksik" in sb or "fatal" in sb or "beracun" in sb:
        hasil.append("toxic")
    if "mudah terbakar" in sb:
        hasil.append("flammable")
    if "oksidator" in sb:
        hasil.append("oxidizing")
    if "bahaya lingkungan" in sb:
        hasil.append("environmental")
    if "iritasi" in sb:
        hasil.append("irritant")
    if "karsinogenik" in sb or "reprotoksik" in sb:
        hasil.append("health_hazard")
    if not hasil:
        hasil.append("safe")
    return list(dict.fromkeys(hasil))

TABEL_GHS = {
    "corrosive":    {"emoji": "🧪", "label": "Korosif",           "color": "#e85d04", "bg": "#fff3e0",
                     "desc": "Dapat merusak/membakar jaringan kulit, mata, dan saluran pernapasan."},
    "toxic":        {"emoji": "☠️", "label": "Toksik/Beracun",    "color": "#7b2d8b", "bg": "#f3e5f5",
                     "desc": "Berbahaya atau mematikan jika tertelan, terhirup, atau terserap kulit."},
    "flammable":    {"emoji": "🔥", "label": "Mudah Terbakar",    "color": "#d62828", "bg": "#fce4e4",
                     "desc": "Dapat dengan mudah terbakar; jauhkan dari sumber panas dan api terbuka."},
    "oxidizing":    {"emoji": "🔶", "label": "Oksidator",         "color": "#e07b00", "bg": "#fff8e1",
                     "desc": "Dapat menyebabkan atau memperparah kebakaran dengan menghasilkan oksigen."},
    "environmental":{"emoji": "🌍", "label": "Bahaya Lingkungan", "color": "#2e7d32", "bg": "#e8f5e9",
                     "desc": "Berbahaya bagi organisme akuatik dan ekosistem perairan."},
    "irritant":     {"emoji": "⚠️", "label": "Iritasi",           "color": "#f0a500", "bg": "#fffde7",
                     "desc": "Dapat menyebabkan iritasi pada kulit, mata, atau saluran pernapasan."},
    "health_hazard":{"emoji": "💀", "label": "Bahaya Kesehatan",  "color": "#880e4f", "bg": "#fce4ec",
                     "desc": "Dapat menyebabkan efek jangka panjang: karsinogenik, mutagenik, atau reprotoksik."},
    "safe":         {"emoji": "✅", "label": "Relatif Aman",       "color": "#1b5e20", "bg": "#e8f5e9",
                     "desc": "Risiko bahaya relatif rendah dalam kondisi pemakaian normal."},
}

def buat_panduan_p3k(nm_bahan: str, sifat_bahan: str, catatan_db: str) -> dict:
    sb = sifat_bahan.lower()
    ada_korosif   = "korosif" in sb
    ada_toksik    = "toksik" in sb or "fatal" in sb
    ada_mudahbakar = "mudah terbakar" in sb
    ada_oksidator = "oksidator" in sb

    if ada_korosif and ada_mudahbakar:
        teks_kulit   = "Segera lepaskan pakaian yang terkontaminasi. Bilas kulit dengan air mengalir selama minimal 15 menit. Jangan gosok area yang terkena. Cari bantuan medis."
        teks_mata    = "DARURAT: Bilas mata dengan air mengalir selama minimal 15 menit sambil membuka kelopak mata lebar. Segera ke dokter mata."
        teks_hirup   = "Pindahkan korban ke ruang segar segera. Jika sesak napas berikan oksigen. Hubungi medis darurat."
        teks_telan   = "JANGAN paksa muntah. Berikan air putih atau susu jika korban sadar. Segera bawa ke IGD."
    elif ada_korosif:
        teks_kulit   = "Bilas segera dengan air bersih mengalir selama minimal 15 menit. Lepas pakaian yang terkontaminasi. Jangan gunakan penetral kimia di kulit."
        teks_mata    = "Bilas mata dengan air mengalir selama minimal 15 menit. Pegang kelopak mata terbuka. Segera ke dokter mata."
        teks_hirup   = "Pindahkan ke udara segar. Kendurkan pakaian di leher. Jika iritasi berlanjut segera minta pertolongan medis."
        teks_telan   = "JANGAN paksa muntah. Berikan segelas air putih. Segera ke IGD dan bawa label/SDS bahan."
    elif ada_toksik:
        teks_kulit   = "Bilas dengan air dan sabun selama 15 menit. Lepas pakaian terkontaminasi. Segera ke dokter."
        teks_mata    = "Bilas dengan air mengalir selama 15 menit. Jangan gosok. Konsultasi dokter segera."
        teks_hirup   = "Segera pindahkan ke udara segar. Berikan pernapasan buatan jika tidak bernapas. Hubungi IGD."
        teks_telan   = "JANGAN paksa muntah untuk racun yang bersifat keras. Segera ke IGD dengan informasi bahan kimia."
    elif ada_mudahbakar:
        teks_kulit   = "Bilas area yang terkena dengan air dan sabun selama 15 menit. Jika ada luka bakar, segera ke UGD."
        teks_mata    = "Bilas mata dengan air mengalir selama 15 menit. Jangan biarkan korban menggosok mata."
        teks_hirup   = "Pindahkan korban ke udara segar. Berikan oksigen jika tersedia. Hubungi medis jika gejala berlanjut."
        teks_telan   = "Jangan paksa muntah (risiko aspirasi ke paru). Berikan air putih dan segera ke dokter."
    else:
        teks_kulit   = "Bilas area yang terkena dengan air mengalir selama 15 menit. Cuci dengan sabun. Cari bantuan medis jika timbul iritasi."
        teks_mata    = "Bilas mata dengan air mengalir selama 15 menit. Hindari menggosok. Hubungi dokter jika ada ketidaknyamanan."
        teks_hirup   = "Pindahkan ke ruang dengan ventilasi baik. Istirahat dan perhatikan gejala. Hubungi medis jika diperlukan."
        teks_telan   = "Berikan segelas air putih. Jangan paksa muntah. Hubungi dokter atau pusat pengendalian racun."

    return {
        "kulit":   teks_kulit,
        "mata":    teks_mata,
        "terhirup": teks_hirup,
        "tertelan": teks_telan,
        "catatan": catatan_db
    }

def buat_prosedur_tumpahan(nm_bahan: str, sifat_bahan: str, teks_tumpahan: str) -> dict:
    sb = sifat_bahan.lower()
    ada_korosif    = "korosif" in sb
    ada_toksik     = "toksik" in sb or "fatal" in sb
    ada_mudahbakar = "mudah terbakar" in sb
    ada_oksidator  = "oksidator" in sb

    daftar_apd = ["Sarung tangan karet/nitril", "Kacamata pelindung"]
    if ada_korosif or ada_toksik:
        daftar_apd += ["Jas lab tertutup", "Sepatu tertutup"]
    if ada_toksik:
        daftar_apd.append("Masker respirator N95/kimia")
    if ada_mudahbakar:
        daftar_apd.append("APD tahan percikan api")

    teks_evakuasi = "Peringatkan personel di sekitar tumpahan." if not ada_toksik else \
                    "EVAKUASI area dengan radius minimal 5 meter dari tumpahan."

    if ada_mudahbakar:
        teks_isolasi = "Matikan semua sumber api, panas, dan percikan listrik. Tutup ventilasi agar uap tidak menyebar."
    elif ada_korosif:
        teks_isolasi = "Hentikan sumber tumpahan jika aman. Batasi penyebaran cairan menggunakan absorben atau pasir."
    else:
        teks_isolasi = "Batasi area tumpahan. Cegah bahan masuk ke saluran air atau drainase."

    teks_bersih  = teks_tumpahan
    teks_buang   = "Masukkan semua material terkontaminasi ke dalam wadah limbah kimia berlabel. Hubungi pengelola limbah B3 institusi."

    return {
        "apd":      daftar_apd,
        "evakuasi": teks_evakuasi,
        "isolasi":  teks_isolasi,
        "bersihkan": teks_bersih,
        "buang":    teks_buang,
    }

DAFTAR_SOAL = [
    {
        "question": "Simbol GHS yang menunjukkan bahan bersifat KOROSIF adalah...",
        "options": ["Tengkorak dan tulang silang", "Tabung meneteskan cairan merusak permukaan", "Nyala api di atas lingkaran", "Tanda seru"],
        "answer": 1,
        "explanation": "Simbol korosif GHS ditunjukkan dengan gambar tabung yang meneteskan cairan ke permukaan dan tangan, menggambarkan kerusakan akibat korosi.",
        "category": "Simbol GHS"
    },
    {
        "question": "Bahan kimia mana yang termasuk kategori LGK 3 (Cairan mudah terbakar)?",
        "options": ["Asam Sulfat", "Barium Klorida", "Aseton", "Natrium Klorida"],
        "answer": 2,
        "explanation": "Aseton (CH₃COCH₃) termasuk LGK 3 (cairan mudah terbakar) karena titik nyalanya sangat rendah (-20°C).",
        "category": "Klasifikasi LGK"
    },
    {
        "question": "Apa tindakan PERTAMA yang harus dilakukan jika bahan korosif mengenai mata?",
        "options": ["Gosok mata dengan kain bersih", "Bilas dengan air mengalir minimal 15 menit", "Teteskan obat tetes mata", "Tutup mata dan istirahat"],
        "answer": 1,
        "explanation": "Bilas segera dengan air mengalir minimal 15 menit sambil membuka kelopak mata lebar-lebar adalah tindakan utama P3K untuk paparan mata.",
        "category": "P3K"
    },
    {
        "question": "Asam Sulfat (H₂SO₄) memiliki sifat bahaya utama...",
        "options": ["Mudah terbakar", "Oksidator lemah", "Sangat korosif", "Ramah lingkungan"],
        "answer": 2,
        "explanation": "Asam sulfat pekat adalah salah satu asam paling korosif, dapat menyebabkan luka bakar parah pada kulit dan jaringan tubuh.",
        "category": "Sifat Kimia"
    },
    {
        "question": "Mengapa Aseton TIDAK boleh disimpan dekat sumber api?",
        "options": ["Karena baunya menyengat", "Karena sangat mudah terbakar (LGK 3)", "Karena bersifat korosif", "Karena bersifat toksik"],
        "answer": 1,
        "explanation": "Aseton memiliki titik nyala -20°C, artinya uapnya dapat terbakar bahkan di suhu ruangan. Ini membuatnya sangat berbahaya di dekat api.",
        "category": "Keselamatan Lab"
    },
    {
        "question": "APD (Alat Pelindung Diri) apa yang WAJIB digunakan saat menangani tumpahan bahan toksik?",
        "options": ["Hanya sarung tangan biasa", "Sarung tangan nitril, kacamata, dan masker respirator", "Hanya masker medis biasa", "Tidak perlu APD untuk tumpahan kecil"],
        "answer": 1,
        "explanation": "Bahan toksik memerlukan perlindungan lengkap: sarung tangan nitril/karet, kacamata pelindung, dan masker respirator sesuai jenis bahaya kimia.",
        "category": "APD"
    },
    {
        "question": "Bahan kimia yang termasuk OKSIDATOR harus disimpan jauh dari...",
        "options": ["Air", "Bahan mudah terbakar dan organik", "Logam", "Basa kuat"],
        "answer": 1,
        "explanation": "Oksidator menghasilkan oksigen yang dapat memperparah kebakaran. Kontak dengan bahan organik atau mudah terbakar sangat berbahaya.",
        "category": "Penyimpanan"
    },
    {
        "question": "Kalium Permanganat (KMnO₄) memiliki warna yang khas, yaitu...",
        "options": ["Biru cerah", "Jingga/oranye", "Ungu gelap/hitam", "Merah muda"],
        "answer": 2,
        "explanation": "KMnO₄ dikenal dengan warna ungu gelap hingga hitam yang sangat khas dan kuat. Larutan encernya berwarna ungu cerah.",
        "category": "Sifat Fisik"
    },
    {
        "question": "Apa yang dimaksud dengan LGK dalam klasifikasi bahan kimia laboratorium?",
        "options": ["Label Golongan Kimia", "Lembar Golongan Kemasan", "Label Golongan Kemasan", "Lembar Guide Kimia"],
        "answer": 2,
        "explanation": "LGK (Label Golongan Kemasan) adalah sistem klasifikasi bahaya berdasarkan sifat fisikokimia bahan untuk keperluan pengemasan dan penyimpanan.",
        "category": "Klasifikasi"
    },
    {
        "question": "Jika seorang rekan laboratorium terhirup uap Amonia (NH₃), tindakan pertama adalah...",
        "options": ["Berikan minum air hangat", "Pindahkan ke udara segar dan longgarkan pakaian", "Tahan napas dan lanjutkan kerja", "Cuci muka dengan sabun"],
        "answer": 1,
        "explanation": "Tindakan pertama untuk korban terhirup zat berbahaya adalah memindahkan ke ruangan berventilasi baik/udara segar dan melonggarkan pakaian yang ketat.",
        "category": "P3K"
    },
    {
        "question": "Bahan kimia mana yang dapat bereaksi eksotermis (menghasilkan panas) saat terkena air?",
        "options": ["Natrium Klorida", "Aluminium Klorida", "Kalsium Karbonat", "Barium Sulfat"],
        "answer": 1,
        "explanation": "AlCl₃ bereaksi dengan air secara eksotermis menghasilkan panas dan gas HCl. Itulah mengapa pengendalian tumpahan tidak boleh langsung menggunakan air.",
        "category": "Reaktivitas"
    },
    {
        "question": "Bahan dengan kode LGK '6.1B' termasuk kategori...",
        "options": ["Cairan mudah terbakar", "Bahan korosif", "Bahan beracun sangat mematikan", "Bahan pengoksidasi"],
        "answer": 2,
        "explanation": "LGK 6.1B menandakan bahan beracun (toxic) dengan tingkat mematikan sangat tinggi. Contohnya adalah Raksa(II) Klorida (HgCl₂).",
        "category": "Klasifikasi LGK"
    },
    {
        "question": "Mengapa Tembaga(II) Sulfat (CuSO₄) TIDAK boleh dibuang ke selokan?",
        "options": ["Karena dapat meledak", "Karena sangat korosif terhadap pipa", "Karena sangat beracun bagi organisme akuatik", "Karena dapat menyebabkan kebakaran"],
        "answer": 2,
        "explanation": "CuSO₄ bersifat toksik lingkungan dan sangat berbahaya bagi organisme akuatik. Pembuangan ke perairan dapat merusak ekosistem air.",
        "category": "Lingkungan"
    },
    {
        "question": "Rumus kimia untuk Kalium Permanganat adalah...",
        "options": ["K₂CrO₄", "KMnO₄", "KNO₃", "K₂Cr₂O₇"],
        "answer": 1,
        "explanation": "KMnO₄ adalah rumus kalium permanganat. K = Kalium, Mn = Mangan, O₄ = 4 atom Oksigen.",
        "category": "Rumus Kimia"
    },
    {
        "question": "Saat menangani tumpahan cairan korosif, mengapa pasir/tanah liat lebih baik daripada kain/kertas?",
        "options": ["Karena lebih murah", "Karena kain/kertas dapat memperburuk reaksi dengan beberapa bahan korosif", "Karena pasir lebih menyerap", "Tidak ada perbedaan"],
        "answer": 1,
        "explanation": "Material organik seperti kertas/kain dapat bereaksi lebih lanjut dengan oksidator dan beberapa asam kuat, berpotensi memperparah bahaya.",
        "category": "Pengendalian Tumpahan"
    },
]

def pasang_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.9rem !important;
        padding: 6px 4px !important;
    }

    .main .block-container { padding-top: 1.5rem; max-width: 1100px; }

    .chem-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 14px 0;
    }
    .info-chip {
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .ghs-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px;
    }
    .step-card {
        border-left: 4px solid #3b82f6;
        background: #f0f7ff;
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    .p3k-tab {
        border-radius: 12px;
        padding: 14px 16px;
        margin: 8px 0;
        font-size: 0.88rem;
        border: 1px solid;
    }
    .hero-stat {
        text-align: center;
        padding: 18px;
        border-radius: 14px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .quiz-option {
        cursor: pointer;
        padding: 10px 14px;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        margin: 6px 0;
        font-size: 0.9rem;
        background: white;
    }
    .sidebar-logo {
        font-family: 'Space Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: white !important;
        padding: 4px 0;
    }
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; }

    hr { border: none; border-top: 1px solid #e2e8f0; margin: 16px 0; }

    [data-testid="metric-container"] { background: white; border-radius: 12px; padding: 12px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

def tampil_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">⚗️ Mini MSDS & Safety Guide</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.75rem;color:#94a3b8!important;margin-top:2px;">v2.0 · Sistem Informasi Kimia</p>', unsafe_allow_html=True)
        st.divider()
        pilihan = st.radio(
            "📌 Navigasi",
            options=["🏠 Beranda", "📋 Mini MSDS", "🚨 Pengendalian Tumpahan", "⚖️ Kalkulator BM", "🧠 Kuis Kimia", "👥 Tentang Kami"],
            label_visibility="collapsed"
        )
        st.divider()
        st.markdown('<p style="font-size:0.72rem;color:#64748b!important;">Politeknik AKA Bogor<br>Analisis Kimia · Kel. 2</p>', unsafe_allow_html=True)
    return pilihan

def halaman_beranda():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a5f 0%, #0f4c75 50%, #1a6fa8 100%);
                border-radius: 20px; padding: 48px 40px; color: white; margin-bottom: 28px;
                position: relative; overflow: hidden;">
      <div style="position:absolute;top:-40px;right:-40px;width:200px;height:200px;
                  background:rgba(255,255,255,0.05);border-radius:50%;"></div>
      <div style="position:absolute;bottom:-60px;left:60%;width:150px;height:150px;
                  background:rgba(255,255,255,0.04);border-radius:50%;"></div>
      <p style="font-size:0.85rem;letter-spacing:3px;text-transform:uppercase;opacity:0.7;margin:0 0 8px;">
        ⚗️ Platform Informasi Kimia Lab
      </p>
      <h1 style="font-size:2.6rem;font-weight:800;margin:0 0 10px;line-height:1.2;color:white;">
        Mini MSDS & Safety Guide
      </h1>
      <p style="font-size:1.15rem;opacity:0.9;margin:0 0 20px;max-width:560px;color:white;">
        Sistem informasi keselamatan bahan kimia yang cepat, lengkap, dan interaktif untuk laboratorium analitik modern.
      </p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <span style="background:rgba(255,255,255,0.15);padding:6px 14px;border-radius:20px;font-size:0.82rem;backdrop-filter:blur(4px);">📊 Mini MSDS</span>
        <span style="background:rgba(255,255,255,0.15);padding:6px 14px;border-radius:20px;font-size:0.82rem;backdrop-filter:blur(4px);">🚨 Prosedur Darurat</span>
        <span style="background:rgba(255,255,255,0.15);padding:6px 14px;border-radius:20px;font-size:0.82rem;backdrop-filter:blur(4px);">⚖️ Kalkulator BM</span>
        <span style="background:rgba(255,255,255,0.15);padding:6px 14px;border-radius:20px;font-size:0.82rem;backdrop-filter:blur(4px);">🧠 Kuis Interaktif</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    jml_bahan    = len(daftar_bahan)
    jml_ghs      = 8
    jml_soal     = len(DAFTAR_SOAL)
    jml_korosif  = sum(1 for b in daftar_bahan if "korosif" in b["sifat"].lower())

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="hero-stat">
          <div style="font-size:2rem;font-weight:800;color:#1e3a5f;">{jml_bahan}</div>
          <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">🧫 Bahan Kimia</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="hero-stat">
          <div style="font-size:2rem;font-weight:800;color:#e85d04;">{jml_ghs}</div>
          <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">⚠️ Simbol GHS</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="hero-stat">
          <div style="font-size:2rem;font-weight:800;color:#d62828;">{jml_korosif}</div>
          <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">🧪 Bahan Korosif</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="hero-stat">
          <div style="font-size:2rem;font-weight:800;color:#7b2d8b;">{jml_soal}</div>
          <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">🧠 Soal Kuis</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    kol_kiri, kol_kanan = st.columns(2)
    with kol_kiri:
        st.markdown("### 💡 Mengapa MSDS Mini ?")
        for ikon, judul, isi in [
            ("🏭", "Kebutuhan Nyata", "Banyak kecelakaan laboratorium terjadi karena minimnya akses cepat terhadap informasi keselamatan bahan kimia."),
            ("📱", "Serba Digital", "Data keselamatan kimia masih banyak tersimpan dalam dokumen fisik yang sulit diakses saat situasi darurat."),
            ("🎓", "Pendidikan Keselamatan", "Mahasiswa kimia perlu platform interaktif untuk mempelajari prosedur K3L laboratorium secara efektif."),
        ]:
            st.markdown(f"""<div class="chem-card" style="padding:14px 18px;">
              <div style="display:flex;align-items:flex-start;gap:12px;">
                <span style="font-size:1.5rem;">{ikon}</span>
                <div><strong style="color:#1e3a5f;">{judul}</strong>
                <p style="margin:4px 0 0;font-size:0.85rem;color:#475569;">{isi}</p></div>
              </div></div>""", unsafe_allow_html=True)

    with kol_kanan:
        st.markdown("### 🌟 Manfaat Platform")
        for ikon, judul, warna_bg, isi in [
            ("⚡", "Akses Cepat",        "#dbeafe", "Cari info lengkap bahan kimia dalam hitungan detik tanpa membuka buku tebal."),
            ("🛡️", "Keselamatan Lab",    "#dcfce7", "Prosedur P3K dan pengendalian tumpahan yang detail membantu respons darurat yang tepat."),
            ("📊", "Data Komprehensif",  "#fef3c7", "74 bahan kimia lab lengkap dengan sifat fisik, klasifikasi LGK, dan simbol GHS."),
            ("🧠", "Belajar Interaktif", "#f3e8ff", "Kuis berbasis konten membantu memahami sifat dan bahaya bahan kimia dengan cara menyenangkan."),
        ]:
            st.markdown(f"""<div style="background:{warna_bg};border-radius:10px;padding:10px 14px;margin:6px 0;display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.3rem;">{ikon}</span>
              <div><strong style="font-size:0.88rem;color:#1e3a5f;">{judul}</strong>
              <p style="margin:2px 0 0;font-size:0.82rem;color:#475569;">{isi}</p></div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🔍 Preview Fitur Utama")
    f1, f2, f3, f4 = st.columns(4)
    daftar_fitur = [
        ("📋", "Mini MSDS",             "#dbeafe", "#1d4ed8",
         "Database 74 bahan kimia lengkap dengan rumus, sifat fisik, wujud, warna, bau & simbol GHS."),
        ("🚨", "Pengendalian Tumpahan", "#fee2e2", "#dc2626",
         "Prosedur langkah demi langkah penanganan tumpahan + P3K detail per jalur paparan."),
        ("⚖️", "Kalkulator BM",         "#d1fae5", "#059669",
         "Hitung berat molekul senyawa secara akurat dengan input jumlah atom per unsur."),
        ("🧠", "Kuis Interaktif",       "#f3e8ff", "#7c3aed",
         f"{len(DAFTAR_SOAL)} soal pilihan ganda seputar sifat, bahaya, APD, dan prosedur kimia lab."),
    ]
    for kolom, (ikon, judul, warna_bg, warna_teks, deskripsi) in zip([f1, f2, f3, f4], daftar_fitur):
        with kolom:
            st.markdown(f"""<div style="background:{warna_bg};border-radius:14px;padding:16px;text-align:center;height:160px;">
              <div style="font-size:2rem;">{ikon}</div>
              <strong style="font-size:0.9rem;color:{warna_teks};">{judul}</strong>
              <p style="font-size:0.78rem;color:#475569;margin-top:6px;">{deskripsi}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📖 Panduan Penggunaan")
    langkah_panduan = [
        ("1", "🧭 Navigasi Sidebar",   "Pilih fitur yang diinginkan melalui menu di sebelah kiri layar.", "#1e3a5f"),
        ("2", "🔍 Mini MSDS",          "Pilih nama bahan kimia dari dropdown untuk melihat informasi lengkap, sifat bahaya, dan simbol GHS.", "#0f4c75"),
        ("3", "🚨 Tumpahan & P3K",     "Pilih bahan kimia yang terlibat insiden untuk mendapatkan prosedur penanganan darurat yang detail.", "#dc2626"),
        ("4", "⚖️ Kalkulator BM",      "Masukkan jumlah atom setiap unsur dalam senyawa untuk menghitung berat molekul secara otomatis.", "#059669"),
        ("5", "🧠 Kuis Kimia",         "Uji pemahaman kamu tentang keselamatan kimia lab melalui 15 soal interaktif yang beragam.", "#7c3aed"),
    ]
    for nomor, judul, isi, warna in langkah_panduan:
        st.markdown(f"""<div style="display:flex;align-items:flex-start;gap:14px;padding:12px 16px;
                        border-radius:12px;border:1px solid #e2e8f0;background:white;margin:6px 0;">
          <div style="background:{warna};color:white;width:28px;height:28px;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;font-weight:700;
                      font-size:0.85rem;flex-shrink:0;">{nomor}</div>
          <div><strong style="color:#1e293b;">{judul}</strong>
          <p style="margin:2px 0 0;font-size:0.84rem;color:#64748b;">{isi}</p></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
                padding:24px 28px;color:white;text-align:center;margin-top:10px;">
      <p style="font-size:0.95rem;margin:0 0 6px;color:white;">⚗️ <strong>Mini MSDS & Safety Guide</strong></p>
      <p style="font-size:0.82rem;opacity:0.8;margin:0;color:white;line-height:1.6;">
        Website ini dikembangkan sebagai proyek Mata Kuliah <strong>Logika dan Pemrograman Komputer</strong>
        untuk membantu akses informasi keselamatan bahan kimia secara cepat, praktis, dan interaktif.<br>
        © 2026 · Kelompok 2 · Program Studi Analisis Kimia · Politeknik AKA Bogor
      </p>
    </div>
    """, unsafe_allow_html=True)


def halaman_msds():
    st.markdown("## 🏠 Sistem Informasi Bahan Kimia — Mini MSDS")
    st.markdown("Pilih bahan kimia untuk menampilkan informasi lengkap termasuk sifat fisik, simbol bahaya GHS, dan klasifikasi LGK.")

    kata_cari = st.text_input("🔍 Cari nama bahan kimia...", placeholder="Contoh: Asam, Etanol, Natrium...")
    hasil_cari = [b for b in daftar_bahan if kata_cari.lower() in b["nama_senyawa"].lower()] if kata_cari else daftar_bahan

    pilihan_dropdown = [f"{b['nama_senyawa']}  ({b['rumus_kimia']})" for b in hasil_cari]
    if not pilihan_dropdown:
        st.warning("Bahan kimia tidak ditemukan. Coba kata kunci lain.")
        return

    label_terpilih = st.selectbox("📌 Pilih Bahan Kimia:", pilihan_dropdown)
    nama_terpilih  = label_terpilih.split("  (")[0]
    bahan          = next(b for b in daftar_bahan if b["nama_senyawa"] == nama_terpilih)

    simbol_ghs  = cari_simbol_ghs(bahan["sifat"])
    warna_utama = TABEL_GHS[simbol_ghs[0]]["color"]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{warna_utama}18,{warna_utama}08);
                border:2px solid {warna_utama}40;border-radius:16px;padding:20px 24px;margin:14px 0;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
        <div>
          <h2 style="margin:0;color:{warna_utama};font-size:1.6rem;">{bahan['nama_senyawa']}</h2>
          <span style="font-family:'Space Mono',monospace;font-size:1.1rem;color:#475569;font-weight:700;">{bahan['rumus_kimia']}</span>
        </div>
        <div>{''.join(f'<span style="background:{TABEL_GHS[g]["bg"]};color:{TABEL_GHS[g]["color"]};padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;margin-left:6px;">{TABEL_GHS[g]["emoji"]} {TABEL_GHS[g]["label"]}</span>' for g in simbol_ghs)}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    kol_ki, kol_ka = st.columns(2)
    properti_kiri = [
        ("🧪 Rumus Molekul", bahan["rumus_kimia"], "#dbeafe"),
        ("🧱 Wujud",         bahan["wujud"],        "#d1fae5"),
        ("🎨 Warna",         bahan["warna"],        "#fef3c7"),
    ]
    properti_kanan = [
        ("👃 Bau",            bahan["bau"],             "#f3e8ff"),
        ("🏷️ Kode LGK",      bahan["lgk"],             "#fee2e2"),
        ("📦 Keterangan LGK", bahan["keterangan_lgk"], "#fff7ed"),
    ]
    with kol_ki:
        for label, nilai, warna_bg in properti_kiri:
            st.markdown(f"""<div style="background:{warna_bg};padding:12px 16px;border-radius:10px;margin:6px 0;">
              <span style="font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">{label}</span>
              <p style="margin:3px 0 0;font-weight:600;color:#1e293b;">{nilai}</p></div>""", unsafe_allow_html=True)
    with kol_ka:
        for label, nilai, warna_bg in properti_kanan:
            st.markdown(f"""<div style="background:{warna_bg};padding:12px 16px;border-radius:10px;margin:6px 0;">
              <span style="font-size:0.78rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">{label}</span>
              <p style="margin:3px 0 0;font-weight:600;color:#1e293b;">{nilai}</p></div>""", unsafe_allow_html=True)

    st.markdown(f"""<div style="background:#fff1f2;border:1px solid #fecdd3;border-radius:12px;padding:14px 18px;margin:10px 0;">
      <span style="font-size:0.78rem;color:#be123c;font-weight:700;text-transform:uppercase;">⚠️ Sifat Bahaya</span>
      <p style="margin:6px 0 0;font-weight:700;color:#be123c;font-size:1rem;">{bahan['sifat']}</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 🔴 Simbol Bahaya GHS")
    kolom_ghs = st.columns(min(len(simbol_ghs), 4))
    for i, kode_ghs in enumerate(simbol_ghs):
        with kolom_ghs[i % len(kolom_ghs)]:
            info = TABEL_GHS[kode_ghs]
            st.markdown(f"""<div style="background:{info['bg']};border:2px solid {info['color']}40;
                            border-radius:14px;padding:16px;text-align:center;height:130px;">
              <div style="font-size:2rem;">{info['emoji']}</div>
              <strong style="color:{info['color']};font-size:0.88rem;">{info['label']}</strong>
              <p style="font-size:0.76rem;color:#64748b;margin:4px 0 0;">{info['desc']}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="background:#f8fafc;border-radius:12px;padding:16px 20px;font-size:0.85rem;color:#475569;border:1px solid #e2e8f0;">
      <strong>ℹ️ Catatan:</strong> Informasi ini bersifat ringkasan (Mini MSDS). Untuk data lengkap, selalu rujuk ke 
      Material Safety Data Sheet (MSDS/SDS) resmi dari produsen atau sumber standar seperti OSHA, ChemIDplus, atau PubChem.
    </div>""", unsafe_allow_html=True)


def halaman_tumpahan():
    st.markdown("## 🚨 Prosedur K3L: Penanganan Tumpahan & P3K")
    st.markdown("Panduan penanganan darurat tumpahan bahan kimia dan pertolongan pertama berdasarkan jalur paparan.")

    pilihan_dropdown = [f"{b['nama_senyawa']}  ({b['rumus_kimia']})" for b in daftar_bahan]
    label_terpilih  = st.selectbox("⚗️ Pilih Bahan Kimia yang Terlibat Insiden:", pilihan_dropdown)
    nama_terpilih   = label_terpilih.split("  (")[0]
    bahan           = next(b for b in daftar_bahan if b["nama_senyawa"] == nama_terpilih)

    simbol_ghs  = cari_simbol_ghs(bahan["sifat"])
    info_utama  = TABEL_GHS[simbol_ghs[0]]
    wc          = info_utama["color"]

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,{wc}22,{wc}0a);border-left:5px solid {wc};
                border-radius:0 14px 14px 0;padding:16px 20px;margin:12px 0;">
      <h3 style="margin:0;color:{wc};">⚠️ Tindakan Darurat: {bahan['nama_senyawa']} ({bahan['rumus_kimia']})</h3>
      <p style="margin:4px 0 0;color:#64748b;font-size:0.88rem;">Sifat Bahaya: <strong style="color:{wc};">{bahan['sifat']}</strong></p>
    </div>""", unsafe_allow_html=True)

    html_badge = " ".join(f'<span style="background:{TABEL_GHS[g]["bg"]};color:{TABEL_GHS[g]["color"]};padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">{TABEL_GHS[g]["emoji"]} {TABEL_GHS[g]["label"]}</span>' for g in simbol_ghs)
    st.markdown(f"<div style='margin:8px 0;'>{html_badge}</div>", unsafe_allow_html=True)

    st.markdown("### 🧯 Prosedur Pengendalian Tumpahan")
    prosedur = buat_prosedur_tumpahan(bahan["nama_senyawa"], bahan["sifat"], bahan["pengendalian_tumpahan"])

    urutan_langkah = [
        ("1", "🚧 EVAKUASI & ISOLASI",    prosedur["evakuasi"],                          "#fef3c7", "#d97706"),
        ("2", "🦺 PAKAI APD",              "Gunakan: " + ", ".join(prosedur["apd"]),      "#dbeafe", "#2563eb"),
        ("3", "🔒 KENDALIKAN PENYEBARAN",  prosedur["isolasi"],                           "#f0fdf4", "#16a34a"),
        ("4", "🧹 BERSIHKAN TUMPAHAN",     prosedur["bersihkan"],                         "#fff7ed", "#ea580c"),
        ("5", "🗑️ PEMBUANGAN LIMBAH",      prosedur["buang"],                             "#fdf4ff", "#9333ea"),
    ]

    for nomor, judul, isi, warna_bg, warna in urutan_langkah:
        st.markdown(f"""
        <div style="background:{warna_bg};border:1px solid {warna}30;border-radius:12px;
                    padding:14px 18px;margin:8px 0;display:flex;align-items:flex-start;gap:12px;">
          <div style="background:{warna};color:white;width:30px;height:30px;border-radius:8px;
                      display:flex;align-items:center;justify-content:center;font-weight:800;
                      font-size:0.82rem;flex-shrink:0;">{nomor}</div>
          <div>
            <strong style="color:{warna};font-size:0.88rem;text-transform:uppercase;letter-spacing:0.5px;">{judul}</strong>
            <p style="margin:4px 0 0;font-size:0.88rem;color:#334155;">{isi}</p>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🩺 Pertolongan Pertama (P3K)")
    st.markdown("Tindakan berdasarkan jalur paparan:")

    data_p3k  = buat_panduan_p3k(bahan["nama_senyawa"], bahan["sifat"], bahan["pertolongan_pertama"])
    tab_p3k   = st.tabs(["🖐️ Kulit", "👁️ Mata", "😮‍💨 Terhirup", "🫀 Tertelan"])
    isi_tab   = [
        ("🖐️", "Terpapar Kulit", data_p3k["kulit"],    "#dbeafe", "#1d4ed8"),
        ("👁️", "Terpapar Mata",  data_p3k["mata"],     "#dcfce7", "#15803d"),
        ("😮‍💨", "Terhirup",      data_p3k["terhirup"], "#fef9c3", "#a16207"),
        ("🫀", "Tertelan",       data_p3k["tertelan"], "#ffe4e6", "#be123c"),
    ]

    for tab, (ikon, judul, konten, warna_bg, warna) in zip(tab_p3k, isi_tab):
        with tab:
            st.markdown(f"""<div style="background:{warna_bg};border:1px solid {warna}30;border-radius:14px;padding:18px 20px;margin:8px 0;">
              <h4 style="color:{warna};margin:0 0 8px;">{ikon} {judul}</h4>
              <p style="margin:0;font-size:0.9rem;color:#334155;line-height:1.7;">{konten}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:14px 18px;margin-top:10px;">
      <strong>📌 Catatan Umum:</strong> {data_p3k["catatan"]}
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:#fee2e2;border-radius:12px;padding:14px 18px;font-size:0.85rem;color:#7f1d1d;">
      <strong>🚑 PENTING:</strong> Informasi ini adalah panduan pertolongan pertama. Untuk kasus serius, 
      segera hubungi IGD / Nomor Darurat <strong>119</strong> atau Poliklinik kampus. Bawa kartu data keselamatan (SDS) 
      bahan kimia kepada petugas medis.
    </div>""", unsafe_allow_html=True)


def halaman_kalkulator():
    st.markdown("## ⚖️ Kalkulator Berat Molekul (BM)")
    st.markdown("Hitung berat molekul senyawa berdasarkan jumlah atom setiap unsur. Massa atom relatif menggunakan standar IUPAC.")

    MASSA_ATOM = {
        "H": 1.008,  "C": 12.011, "N": 14.007, "O": 15.999,
        "Na": 22.990, "Mg": 24.305, "Al": 26.982, "S": 32.06,
        "Cl": 35.45,  "K": 39.098, "Ca": 40.078, "Fe": 55.845,
        "Cu": 63.546, "Zn": 65.38, "Br": 79.904, "Ag": 107.868,
        "Ba": 137.327, "Pb": 207.2, "Hg": 200.592, "Cr": 51.996,
        "Mn": 54.938, "P": 30.974, "I": 126.904,  "Sn": 118.71,
    }

    st.markdown("""<div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:12px;padding:14px 18px;margin-bottom:16px;font-size:0.85rem;color:#0369a1;">
      💡 <strong>Petunjuk:</strong> Masukkan jumlah atom setiap unsur dalam senyawa. Kosongkan atau isikan 0 untuk unsur yang tidak ada.
    </div>""", unsafe_allow_html=True)

    kelompok_unsur = [
        ("Nonlogam Umum",      [("H","Hidrogen"),("C","Karbon"),("N","Nitrogen"),("O","Oksigen"),("S","Belerang"),("P","Fosfor")]),
        ("Halogen",            [("Cl","Klor"),("Br","Brom"),("I","Iodium")]),
        ("Logam Alkali",       [("Na","Natrium"),("K","Kalium")]),
        ("Logam Alkali Tanah", [("Mg","Magnesium"),("Ca","Kalsium"),("Ba","Barium")]),
        ("Logam Transisi",     [("Fe","Besi"),("Cu","Tembaga"),("Zn","Seng"),("Cr","Kromium"),("Mn","Mangan"),("Ag","Perak"),("Pb","Timbal"),("Hg","Raksa"),("Al","Aluminium"),("Sn","Timah")]),
    ]

    jumlah_atom = {}
    for nama_grup, isi_grup in kelompok_unsur:
        st.markdown(f"**{nama_grup}**")
        baris = st.columns(len(isi_grup))
        for i, (simbol, nama_unsur) in enumerate(isi_grup):
            with baris[i]:
                nilai = st.number_input(f"{simbol}\n({nama_unsur})", min_value=0, value=0, step=1, key=f"atom_{simbol}")
                jumlah_atom[simbol] = nilai

    st.markdown("---")

    if st.button("⚖️ Hitung Berat Molekul", type="primary", use_container_width=True):
        bm_total   = sum(jumlah_atom[sim] * MASSA_ATOM[sim] for sim in jumlah_atom)
        atom_aktif = [(sim, n) for sim, n in jumlah_atom.items() if n > 0]

        if not atom_aktif:
            st.warning("⚠️ Masukkan minimal satu atom untuk menghitung BM.")
        else:
            rumus_str = "".join(f"{sim}{n if n > 1 else ''}" for sim, n in atom_aktif)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e3a5f,#0f4c75);color:white;border-radius:16px;
                        padding:24px;text-align:center;margin:16px 0;">
              <p style="margin:0;font-size:0.85rem;opacity:0.8;">Rumus dari input:</p>
              <p style="font-family:'Space Mono',monospace;font-size:1.4rem;font-weight:700;margin:4px 0;">{rumus_str}</p>
              <p style="margin:8px 0 4px;font-size:0.85rem;opacity:0.8;">Berat Molekul:</p>
              <p style="font-size:2.5rem;font-weight:800;margin:0;">{bm_total:.3f}</p>
              <p style="font-size:0.9rem;opacity:0.8;margin:0;">g/mol</p>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### 📊 Rincian Perhitungan")
            akumulasi = 0
            for sim, n in atom_aktif:
                bobot = n * MASSA_ATOM[sim]
                akumulasi += bobot
                persen = (bobot / bm_total * 100)
                st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                                padding:8px 14px;border-radius:8px;background:#f8fafc;border:1px solid #e2e8f0;margin:4px 0;">
                  <span style="font-weight:600;">{sim} ({n} atom × {MASSA_ATOM[sim]} g/mol)</span>
                  <span style="color:#1e3a5f;font-weight:700;">{bobot:.3f} g/mol <span style="color:#64748b;font-size:0.82rem;">({persen:.1f}%)</span></span>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:10px 14px;
                            border-radius:8px;background:#1e3a5f;color:white;margin-top:6px;font-weight:700;">
              <span>Total BM</span><span>{akumulasi:.3f} g/mol</span></div>""", unsafe_allow_html=True)


def halaman_kuis():
    st.markdown("## 🧠 Kuis Keselamatan Kimia Lab")
    st.markdown("Uji pemahamanmu tentang sifat, bahaya, APD, dan prosedur K3L laboratorium.")

    if "kuis_mulai" not in st.session_state:
        st.session_state.kuis_mulai = False
    if "kuis_nilai" not in st.session_state:
        st.session_state.kuis_nilai = 0
    if "kuis_nomor" not in st.session_state:
        st.session_state.kuis_nomor = 0
    if "kuis_dijawab" not in st.session_state:
        st.session_state.kuis_dijawab = False
    if "kuis_pilihan" not in st.session_state:
        st.session_state.kuis_pilihan = None
    if "kuis_soal" not in st.session_state:
        st.session_state.kuis_soal = []
    if "kuis_selesai" not in st.session_state:
        st.session_state.kuis_selesai = False

    if not st.session_state.kuis_mulai:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#4c1d95,#7c3aed);color:white;border-radius:20px;padding:32px;text-align:center;margin:16px 0;">
          <div style="font-size:3rem;">🧠</div>
          <h2 style="color:white;margin:8px 0;">Kuis Keselamatan Kimia</h2>
          <p style="opacity:0.9;color:white;">15 soal pilihan ganda seputar sifat kimia, GHS, APD, P3K, dan penanganan tumpahan.</p>
        </div>""", unsafe_allow_html=True)

        daftar_kategori = set(s["category"] for s in DAFTAR_SOAL)
        kolom_kat = st.columns(len(daftar_kategori))
        for i, kat in enumerate(daftar_kategori):
            jml = sum(1 for s in DAFTAR_SOAL if s["category"] == kat)
            with kolom_kat[i % len(kolom_kat)]:
                st.markdown(f"""<div style="text-align:center;padding:12px;background:#f3e8ff;border-radius:10px;margin:4px 0;">
                  <strong style="color:#7c3aed;font-size:0.85rem;">{kat}</strong>
                  <p style="margin:2px 0;font-size:0.8rem;color:#64748b;">{jml} soal</p></div>""", unsafe_allow_html=True)

        if st.button("▶️ Mulai Kuis", type="primary", use_container_width=True):
            st.session_state.kuis_mulai   = True
            st.session_state.kuis_selesai = False
            st.session_state.kuis_nilai   = 0
            st.session_state.kuis_nomor   = 0
            st.session_state.kuis_dijawab = False
            st.session_state.kuis_pilihan = None
            acak = DAFTAR_SOAL.copy()
            random.shuffle(acak)
            st.session_state.kuis_soal = acak[:min(10, len(acak))]
            st.rerun()
        return

    if st.session_state.kuis_selesai:
        soal_dimainkan = st.session_state.kuis_soal
        nilai_akhir    = st.session_state.kuis_nilai
        total_soal     = len(soal_dimainkan)
        persentase     = nilai_akhir / total_soal * 100
        warna_hasil    = "#16a34a" if persentase >= 70 else "#d97706" if persentase >= 50 else "#dc2626"
        pesan          = "🏆 Luar Biasa!" if persentase >= 80 else "👍 Bagus!" if persentase >= 60 else "📚 Perlu Belajar Lagi"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{warna_hasil}15,{warna_hasil}05);border:2px solid {warna_hasil}40;
                    border-radius:20px;padding:32px;text-align:center;margin:16px 0;">
          <div style="font-size:3rem;">{pesan.split()[0]}</div>
          <h2 style="color:{warna_hasil};margin:8px 0;">{pesan[2:]}</h2>
          <p style="font-size:3rem;font-weight:800;color:{warna_hasil};margin:8px 0;">{nilai_akhir}/{total_soal}</p>
          <p style="color:#64748b;">Skor: {persentase:.0f}%</p>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Ulangi Kuis", use_container_width=True):
            st.session_state.kuis_mulai   = False
            st.session_state.kuis_selesai = False
            st.rerun()
        return

    soal_aktif = st.session_state.kuis_soal
    no_sekarang = st.session_state.kuis_nomor
    soal        = soal_aktif[no_sekarang]

    kemajuan = no_sekarang / len(soal_aktif)
    st.markdown(f"""<div style="background:#e2e8f0;border-radius:10px;height:8px;margin-bottom:16px;">
      <div style="background:#7c3aed;width:{kemajuan*100:.0f}%;height:8px;border-radius:10px;transition:width 0.3s;"></div>
    </div>""", unsafe_allow_html=True)

    warna_kat = {
        "Simbol GHS": "#dc2626", "Klasifikasi LGK": "#d97706", "P3K": "#16a34a",
        "Sifat Kimia": "#2563eb", "Keselamatan Lab": "#7c3aed", "APD": "#0891b2",
        "Penyimpanan": "#db2777", "Sifat Fisik": "#0284c7", "Klasifikasi": "#6d28d9",
        "Pengendalian Tumpahan": "#b45309", "Lingkungan": "#15803d",
        "Reaktivitas": "#be185d", "Rumus Kimia": "#1d4ed8"
    }.get(soal["category"], "#475569")

    st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:16px;padding:24px;margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <span style="background:{warna_kat}15;color:{warna_kat};padding:4px 12px;border-radius:20px;font-size:0.78rem;font-weight:700;">{soal['category']}</span>
        <span style="color:#94a3b8;font-size:0.85rem;">Soal {no_sekarang+1} dari {len(soal_aktif)}</span>
      </div>
      <h3 style="margin:0;color:#1e293b;font-size:1.05rem;line-height:1.5;">{soal['question']}</h3>
    </div>""", unsafe_allow_html=True)

    sudah_jawab     = st.session_state.kuis_dijawab
    pilihan_user    = st.session_state.kuis_pilihan

    for i, opsi in enumerate(soal["options"]):
        if sudah_jawab:
            if i == soal["answer"]:
                bg, border, warna_teks = "#dcfce7", "#16a34a", "#15803d"
                awalan = "✅ "
            elif i == pilihan_user and pilihan_user != soal["answer"]:
                bg, border, warna_teks = "#fee2e2", "#dc2626", "#dc2626"
                awalan = "❌ "
            else:
                bg, border, warna_teks = "#f8fafc", "#e2e8f0", "#64748b"
                awalan = ""
            st.markdown(f"""<div style="background:{bg};border:2px solid {border};border-radius:10px;
                            padding:12px 16px;margin:6px 0;color:{warna_teks};font-weight:{'700' if i == soal['answer'] or i == pilihan_user else '400'};">
              {awalan}{opsi}</div>""", unsafe_allow_html=True)
        else:
            if st.button(f"{opsi}", key=f"opsi_{no_sekarang}_{i}", use_container_width=True):
                st.session_state.kuis_pilihan = i
                st.session_state.kuis_dijawab = True
                if i == soal["answer"]:
                    st.session_state.kuis_nilai += 1
                st.rerun()

    if sudah_jawab:
        st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 18px;margin:10px 0;">
          <strong style="color:#15803d;">💡 Penjelasan:</strong>
          <p style="margin:4px 0 0;color:#334155;font-size:0.88rem;">{soal['explanation']}</p>
        </div>""", unsafe_allow_html=True)

        if no_sekarang + 1 < len(soal_aktif):
            if st.button("➡️ Soal Berikutnya", type="primary", use_container_width=True):
                st.session_state.kuis_nomor   += 1
                st.session_state.kuis_dijawab  = False
                st.session_state.kuis_pilihan  = None
                st.rerun()
        else:
            if st.button("🏁 Lihat Hasil", type="primary", use_container_width=True):
                st.session_state.kuis_selesai = True
                st.rerun()


def halaman_tentang():
    st.markdown("## 👥 Tentang Kami")

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a5f,#0f4c75);color:white;border-radius:18px;padding:28px 32px;margin-bottom:24px;">
      <h3 style="color:white;margin:0 0 8px;">⚗️ Mini MSDS & Safety Guide</h3>
      <p style="opacity:0.9;margin:0 0 12px;color:white;">
        Proyek ini dikembangkan sebagai tugas akhir Mata Kuliah <strong>Logika dan Pemrograman Komputer</strong>
        oleh mahasiswa Program Studi Analisis Kimia, Politeknik AKA Bogor.
      </p>
      <p style="opacity:0.8;font-size:0.88rem;margin:0;color:white;">
        Tujuan: menyediakan platform digital yang membantu mahasiswa dan praktisi laboratorium 
        mengakses informasi keselamatan bahan kimia (K3L) secara cepat, akurat, dan interaktif.
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown("### 👨‍🔬 Kelompok 2 — Anggota Tim")

    anggota_tim = [
        ("A", "ACHDES 'AZILLA ZACHROTUL SYITA", "Analisis Kimia", "#e85d04", "#fff3e0"),
        ("A", "ATHA MAHARDIKA NAWAN",            "Analisis Kimia", "#1d4ed8", "#dbeafe"),
        ("M", "MANAHEL ARIELLA PERTA",           "Analisis Kimia", "#7c3aed", "#f3e8ff"),
        ("N", "NAILA PUTRI ZAHRA",               "Analisis Kimia", "#0891b2", "#e0f2fe"),
        ("S", "SALWA SAFAANAH",                  "Analisis Kimia", "#16a34a", "#dcfce7"),
    ]

    for huruf, nama, prodi, warna, warna_bg in anggota_tim:
        st.markdown(f"""
        <div style="background:{warna_bg};border:1px solid {warna}30;border-radius:14px;
                    padding:16px 20px;margin:8px 0;display:flex;align-items:center;gap:16px;">
          <div style="background:{warna};color:white;width:44px;height:44px;border-radius:50%;
                      display:flex;align-items:center;justify-content:center;font-weight:800;
                      font-size:1.1rem;flex-shrink:0;">{huruf}</div>
          <div>
            <strong style="color:{warna};font-size:0.95rem;">{nama}</strong>
            <p style="margin:3px 0 0;font-size:0.82rem;color:#64748b;">🎓 Program Studi {prodi}</p>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    kol1, kol2 = st.columns(2)
    with kol1:
        st.markdown("""
        <div class="chem-card">
          <h4 style="margin:0 0 10px;color:#1e3a5f;">🏛️ Institusi</h4>
          <p style="margin:4px 0;"><strong>Politeknik AKA Bogor</strong></p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">Akademi Kimia Analis Bogor</p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">Kementerian Perindustrian RI</p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">📍 Bogor, Jawa Barat</p>
        </div>""", unsafe_allow_html=True)
    with kol2:
        st.markdown("""
        <div class="chem-card">
          <h4 style="margin:0 0 10px;color:#1e3a5f;">📚 Mata Kuliah</h4>
          <p style="margin:4px 0;"><strong>Logika dan Pemrograman Komputer</strong></p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">Program Studi: D3 Analisis Kimia</p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">Platform: Python + Streamlit</p>
          <p style="margin:4px 0;font-size:0.85rem;color:#64748b;">🗓️ Tahun Akademik 2025/2026</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
                padding:22px 28px;color:white;text-align:center;">
      <p style="font-size:0.95rem;margin:0 0 6px;color:white;">⚗️ <strong>Mini MSDS & Safety Guide v2.0</strong></p>
      <p style="font-size:0.82rem;opacity:0.8;margin:0;color:white;line-height:1.7;">
        Website ini dikembangkan sebagai proyek Mata Kuliah <strong>Logika dan Pemrograman Komputer</strong>
        untuk membantu akses informasi keselamatan bahan kimia secara cepat, praktis, dan interaktif.<br>
        © 2026 · Kelompok 2 · Program Studi Analisis Kimia · Politeknik AKA Bogor
      </p>
    </div>""", unsafe_allow_html=True)


def jalankan():
    pasang_css()
    halaman = tampil_sidebar()

    if "Beranda" in halaman:
        halaman_beranda()
    elif "Mini MSDS" in halaman:
        halaman_msds()
    elif "Tumpahan" in halaman:
        halaman_tumpahan()
    elif "Kalkulator" in halaman:
        halaman_kalkulator()
    elif "Kuis" in halaman:
        halaman_kuis()
    elif "Tentang" in halaman:
        halaman_tentang()


if __name__ == "__main__":
    jalankan()
