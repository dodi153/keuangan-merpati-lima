import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Keuangan Merpati 5", layout="wide", page_icon="🐦")

# --- FUNGSI LOAD DATA ---
def load_csv(file_name, skip=0):
    try:
        # Membaca file CSV yang Anda unggah
        return pd.read_csv(file_name, skiprows=skip)
    except:
        return None

# --- SIDEBAR ---
st.sidebar.title("Merpati 5 Finance")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Pilih Layanan", 
    ["🏠 Dashboard Utama", "💰 Status Iuran Warga", "📑 Laporan Cash Flow", "📂 Data Warga"])

# --- MENU 1: DASHBOARD UTAMA ---
if menu == "🏠 Dashboard Utama":
    st.title("📊 Dashboard Keuangan")
    
    # Menampilkan Ringkasan (Data diambil dari Laporan Posisi Kas Anda)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Saldo Tersedia", "Rp 5.326.500")
    with col2:
        st.metric("Saldo Kas Berjalan (Feb)", "Rp 4.201.500")
    with col3:
        st.metric("Agenda Belum Realisasi", "Rp 5.150.000", delta="- (Kurang)")

    st.markdown("---")
    st.subheader("⚠️ Agenda Mendesak (Sebelum Puasa)")
    agenda = pd.DataFrame({
        "Deskripsi": ["Pemasangan Portal", "Jasa Potong Rumput"],
        "Anggaran": ["Rp 4.750.000", "Rp 400.000"],
        "Prioritas": ["Tinggi", "Sedang"]
    })
    st.table(agenda)

# --- MENU 2: STATUS IURAN WARGA ---
elif menu == "💰 Status Iuran Warga":
    st.header("Rekap Iuran Buku 2026")
    
    # Membaca data dari file Kas Gang
    df_iuran = load_csv("Keuangan MERPATI 5 2026 (1).xlsx - Kas Gang.csv", skip=2)
    
    if df_iuran is not None:
        # Bersihkan kolom kosong
        df_iuran = df_iuran.dropna(subset=['Nama KK', 'No. Rumah'])
        
        search = st.text_input("Cari Nama atau No Rumah:")
        if search:
            df_iuran = df_iuran[df_iuran['Nama KK'].astype(str).str.contains(search, case=False) | 
                                df_iuran['No. Rumah'].astype(str).str.contains(search, case=False)]
        
        st.dataframe(df_iuran, use_container_width=True)
    else:
        st.error("File 'Kas Gang' tidak ditemukan.")

# --- MENU 3: CASH FLOW ---
elif menu == "📑 Laporan Cash Flow":
    st.header("Arus Kas Bulanan")
    bln = st.selectbox("Pilih Bulan", ["Januari", "Februari"])
    
    file_cf = f"Keuangan MERPATI 5 2026 (1).xlsx - Cash Flow {bln}.csv"
    df_cf = load_csv(file_cf, skip=5)
    
    if df_cf is not None:
        st.write(f"Detail Transaksi {bln} 2026")
        st.dataframe(df_cf.dropna(how='all', axis=1).dropna(how='all', axis=0))
    else:
        st.warning(f"Data Cash Flow {bln} belum tersedia.")

# --- MENU 4: DATA WARGA ---
elif menu == "📂 Data Warga":
    st.header("Database Warga Merpati 5")
    df_warga = load_csv("Keuangan MERPATI 5 2026 (1).xlsx - Data Gang.csv", skip=2)
    
    if df_warga is not None:
        st.dataframe(df_warga[['Nama KK', 'No. Rumah']].dropna())
    else:
        st.error("Data tidak ditemukan.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.info("Tips: Update file CSV di GitHub untuk memperbarui data aplikasi.")