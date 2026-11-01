# Dashboard Tren Populasi Indonesia (Flask + Chart.js)

Kode studi kasus visualisasi data interaktif untuk mata kuliah Praktik Web Aplikasi. Data pada `data/populasi_indonesia.csv` berisi data historis populasi dari tahun 1960 hingga 2025.

## Menjalankan

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000 di browser. Chart.js dimuat dari CDN, jadi memerlukan koneksi internet.

## Endpoint

| URL | Isi |
|---|---|
| `/` | Halaman dashboard |
| `/api/ringkasan` | Populasi terbaru, persentase pertumbuhan, rata-rata populasi |
| `/api/populasi` | Daftar tahun dan jumlah populasi untuk grafik |

Semua endpoint `/api/...` menerima filter query string `?mulai=1960&akhir=2025`.