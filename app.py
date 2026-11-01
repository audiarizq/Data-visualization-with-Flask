"""Dashboard tren populasi Indonesia.

Jalankan dari folder week8 dengan ``python app.py``, lalu buka
http://127.0.0.1:5000.
"""
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder="template")

# File menggunakan titik koma sebagai pemisah kolom.
df = pd.read_csv(BASE_DIR / "data" / "populasi_indonesia.csv", sep=";")
df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]
df["tahun"] = df["tahun"].astype(int)
df["jumlah_penduduk"] = df["jumlah_penduduk"].astype(int)


def data_terfilter():
    """Kembalikan data sesuai rentang tahun pada query string."""
    data = df
    mulai = request.args.get("mulai", type=int)
    akhir = request.args.get("akhir", type=int)
    if mulai is not None:
        data = data[data["tahun"] >= mulai]
    if akhir is not None:
        data = data[data["tahun"] <= akhir]
    return data


@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        tahun_min=int(df["tahun"].min()),
        tahun_max=int(df["tahun"].max()),
    )


@app.route("/api/ringkasan")
def ringkasan():
    data = data_terfilter()
    if data.empty:
        return jsonify(error="Rentang tahun tidak memiliki data"), 400

    awal = int(data.iloc[0]["jumlah_penduduk"])
    terbaru = int(data.iloc[-1]["jumlah_penduduk"])
    pertumbuhan = ((terbaru - awal) / awal * 100) if awal else 0
    return jsonify(
        tahun_awal=int(data.iloc[0]["tahun"]),
        tahun_terbaru=int(data.iloc[-1]["tahun"]),
        populasi_terbaru=terbaru,
        pertumbuhan=round(pertumbuhan, 2),
        rata_rata_tahunan=round(float(data["jumlah_penduduk"].mean())),
    )


@app.route("/api/populasi")
def populasi():
    data = data_terfilter()
    return jsonify(
        tahun=data["tahun"].tolist(),
        populasi=data["jumlah_penduduk"].tolist(),
    )


if __name__ == "__main__":
    app.run(debug=True)
