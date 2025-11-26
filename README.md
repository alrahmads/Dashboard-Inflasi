# Dashboard Inflasi Indonesia

**Platform Analisis dan Prediksi Tingkat Inflasi Berbasis Machine Learning**

## 📌 Tentang Proyek

Dashboard Inflasi Indonesia adalah aplikasi web interaktif yang dirancang untuk menganalisis dan memprediksi tingkat inflasi di Indonesia menggunakan pendekatan regresi linier dan nonlinier. Proyek ini dikembangkan sebagai final project mata kuliah **Workshop Analitika Data Terapan** di Politeknik Elektronika Negeri Surabaya.

Platform ini menggabungkan analisis statistik mendalam dengan machine learning untuk memberikan insights berharga tentang dinamika inflasi dan faktor-faktor ekonomi makro yang mempengaruhinya.

## ✨ Fitur Utama

### 1. **Filter Data Periode** 📅
- Pilih rentang waktu analisis (tahun dan bulan mulai/akhir)
- Tampilan dinamis berdasarkan periode yang dipilih
- Update informasi secara real-time

### 2. **Indikator Makroekonomi Terkini** 📊
Menampilkan 7 metrik utama pada periode terakhir yang dipilih:
- **Inflasi Terkini**: Tingkat inflasi (%)
- **BI Rate**: Suku bunga acuan Bank Indonesia (%)
- **Kurs USD/IDR**: Nilai tukar rupiah terhadap dolar
- **Uang Beredar**: Jumlah uang yang beredar di masyarakat (Triliun Rp)
- **Investasi**: Total investasi (Triliun Rp)
- **Ekspor**: Total nilai ekspor (Miliar USD)
- **Impor**: Total nilai impor (Miliar USD)

### 3. **Tren Utama** 📈
- Visualisasi tren inflasi dengan target BI (2.5-3.0%)
- Indikator kinerja (rata-rata, max, min, volatilitas)
- Analisis tren pergerakan inflasi
- Pola musiman berdasarkan bulan

### 4. **Analisis Komparatif** 🔄
- Perbandingan inflasi vs variabel ekonomi lainnya
- Grafik dual-axis untuk multiple variables
- Scatter plot dengan trendline
- Analisis korelasi antar variabel

### 5. **Model & Prediksi** 🤖
- Perbandingan model regresi linier dan nonlinier
- Visualisasi aktual vs prediksi inflasi
- Metrik evaluasi (MAE, RMSE, R²)
- **Fitur simulasi interaktif**: Masukkan nilai variabel ekonomi untuk prediksi inflasi

### 6. **Data Explorer** 📂
- Tabel data time series yang dapat disortir
- Numeric summary dan category breakdown
- Export data dalam format CSV, JSON, dan Excel

## 🚀 Cara Penggunaan

### Prerequisites
```bash
Python 3.8+
pip
```

### Instalasi

1. Clone repository
```bash
git clone https://github.com/username/dashboard-inflasi-indonesia.git
cd dashboard-inflasi-indonesia
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

### Struktur File

```
dashboard-inflasi-indonesia/
├── app.py                          # Main application
├── ridge_model.pkl                 # Pre-trained Ridge Regression model
├── Data_inflasi.json               # Data inflasi (format JSON)
├── requirements.txt                # Dependencies
└── README.md
```

## 📊 Data & Variabel

### Periode Data
- **Rentang**: Januari 2010 - Desember 2024 (180 observasi bulanan)
- **Sumber**: Badan Pusat Statistik (BPS) & Federal Reserve Economic Data (FRED)
- **Format**: Time series bulanan

### Variabel yang Digunakan

| Variabel | Keterangan | Satuan |
|----------|-----------|--------|
| **Y: Inflasi** | Tingkat inflasi | % |
| **X1: BI Rate** | Suku bunga acuan Bank Indonesia | % |
| **X2: Kurs** | Nilai tukar IDR/USD | Rp per USD |
| **X3: Uang Beredar (M2)** | Jumlah uang beredar | Miliar Rp |
| **X4: Investasi** | Total investasi domestik | Miliar Rp |
| **X5: Ekspor** | Total nilai ekspor | Juta USD |
| **X6: Impor** | Total nilai impor | Juta USD |

## 🔬 Metodologi & Model

### Teknik Feature Engineering
1. **Ekstraksi Fitur Waktu**: Month, Year, Cyclical Encoding (sin/cos)
2. **Lag Features**: Inflasi lag 1/3/12, BI Rate lag 1/3, Kurs lag 1/3
3. **Rolling Statistics**: 3-month moving average, 12-month std deviation
4. **Log Transform**: Normalisasi distribusi variabel skewed

### Model yang Digunakan

#### Model Regresi Linear
- **Ordinary Least Squares (OLS)**: Baseline model
- **Lasso Regression**: L1 regularization untuk feature selection
- **Ridge Regression**: L2 regularization untuk mengatasi multikolinearitas

#### Model Regresi Non-Linear
- **Support Vector Regression (SVR)**: RBF & Linear kernel
- **Random Forest Regressor**: Ensemble-based tree model
- **XGBoost Regressor**: Gradient boosting untuk prediksi kompleks

### Evaluasi Model

**Metrik Evaluasi:**
- **MAE (Mean Absolute Error)**: Rata-rata kesalahan absolut
- **RMSE (Root Mean Squared Error)**: Akar dari rata-rata kuadrat error
- **R² (Coefficient of Determination)**: Proporsi variansi yang dijelaskan

**Hasil Model Terbaik (Ridge Regression):**
- MAE: 0.2531
- RMSE: 0.3144
- R²: 0.9423 (model menjelaskan 94.23% variansi inflasi)
**Dikembangkan untuk Workshop Analitika Data Terapan** ✨

*Terakhir diupdate: Desember 2024*
