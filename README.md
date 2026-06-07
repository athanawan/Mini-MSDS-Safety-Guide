# ⚗️ ChemAssist Lab — Sistem Informasi Keselamatan Bahan Kimia

> Proyek Mata Kuliah Logika dan Pemrograman Komputer  
> Kelompok 2 · Program Studi Analisis Kimia · Politeknik AKA Bogor

---

## Deskripsi

**ChemAssist Lab** adalah platform web interaktif berbasis Python (Streamlit) yang menyediakan:
- 📋 **Mini MSDS** — Informasi lengkap 74 bahan kimia lab (sifat fisik, GHS, LGK)
- 🚨 **Pengendalian Tumpahan** — Prosedur darurat + P3K detail per jalur paparan
- ⚖️ **Kalkulator Berat Molekul** — Hitung BM berdasarkan input atom
- 🧠 **Kuis Interaktif** — 15 soal seputar keselamatan kimia laboratorium
- 👥 **Tentang Kami** — Profil tim pengembang

---

## Cara Deploy ke Streamlit Cloud

### 1. Siapkan Repository GitHub
```
Struktur folder:
├── app.py
├── database_kimia.json
├── requirements.txt
└── README.md
```

### 2. Push ke GitHub
```bash
git init
git add .
git commit -m "Initial commit: ChemAssist Lab"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

### 3. Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository, branch `main`, dan file `app.py`
5. Klik **"Deploy"**

---

## 👥 Tim Pengembang — Kelompok 2

| No | Nama |
|----|------|
| 1 | ACHDES 'AZILLA ZACHROTUL SYITA |
| 2 | ATHA MAHARDIKA NAWAN |
| 3 | MANAHEL ARIELLA PERTA |
| 4 | NAILA PUTRI ZAHRA |
| 5 | SALWA SAFAANAH |

**Program Studi:** D3 Analisis Kimia  
**Institusi:** Politeknik AKA Bogor  
**Mata Kuliah:** Logika dan Pemrograman Komputer  

---

## 🛠️ Teknologi

- **Python 3.14.3+**
- **Streamlit** — Web framework
- **JSON** — Database bahan kimia

---

## 📄 Lisensi

Proyek akademik — Politeknik AKA Bogor © 2026
