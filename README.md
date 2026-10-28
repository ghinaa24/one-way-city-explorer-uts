
# One-Way City Explorer

## 1. Deskripsi Proyek

One-Way City Explorer merupakan aplikasi graf interaktif untuk
mempelajari pengaruh arah jalan terhadap keterjangkauan dan
panjang lintasan perjalanan.

Pengguna dapat memilih titik asal dan tujuan, melihat lintasan
yang tersedia, membalik arah suatu ruas jalan, serta membandingkan
hasil perjalanan sebelum dan sesudah perubahan.

Proyek ini dibuat untuk memenuhi tugas Ujian Tengah Semester (UTS)
yang mengintegrasikan pemodelan graf, algoritma pencarian lintasan,
visualisasi, interaksi, dan validasi komputasi.

## 2. Tujuan

1. Memodelkan jaringan jalan menggunakan graf berarah.
2. Menentukan apakah tujuan dapat dicapai dari titik asal.
3. Menemukan lintasan terpendek berdasarkan panjang ruas jalan.
4. Mengamati pengaruh pembalikan arah jalan terhadap lintasan.
5. Memvalidasi hasil perhitungan menggunakan NetworkX.

## 3. Teknologi yang Digunakan

- Python
- Streamlit
- NetworkX
- Pandas
- Matplotlib

## 4. Struktur Folder

```text
one-way-city-explorer/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── road_network.csv
```

## 5. Dataset

Dataset yang digunakan adalah `road_network.csv`, yang memuat
atribut ruas jalan seperti identitas ruas, nama jalan, panjang
jalan, dan informasi koordinat jika tersedia.

Karena dataset belum menyediakan informasi arah satu arah
secara memadai dan hubungan geografis antarruas belum terverifikasi,
aplikasi menggunakan topologi jaringan demonstrasi dengan 12 simpul.

Dengan demikian, atribut jalan berasal dari dataset, sedangkan
hubungan antarsimpul dan arah awal merupakan bagian dari simulasi.
Hasil aplikasi tidak dimaksudkan untuk merepresentasikan kondisi
jalan nyata secara langsung.

## 6. Model Graf

Jaringan dimodelkan menggunakan graf berarah (*Directed Graph*)
dengan NetworkX.

- **Simpul (node):** titik persimpangan atau lokasi abstrak.
- **Sisi berarah (directed edge):** hubungan perjalanan dari
  satu simpul menuju simpul lainnya.
- **Bobot sisi:** panjang ruas jalan dalam kilometer.
- **Lintasan:** urutan simpul yang terhubung mengikuti arah sisi.

Jumlah simpul dalam model demonstrasi adalah 12, yaitu A sampai L.

## 7. Algoritma

### a. Keterjangkauan

Fungsi `networkx.has_path()` digunakan untuk memeriksa apakah
terdapat lintasan berarah dari titik asal menuju tujuan.

### b. Lintasan terpendek

Fungsi `networkx.shortest_path()` digunakan untuk mencari
lintasan dengan total bobot panjang jalan terkecil.

### c. Pembalikan arah

Satu sisi `(u, v)` dapat diubah menjadi `(v, u)`. Setelah
perubahan dilakukan, aplikasi menghitung ulang lintasan dan
membandingkan hasilnya dengan kondisi awal.

### d. Validasi

Setiap langkah lintasan diperiksa untuk memastikan sisi berarah
yang digunakan benar-benar tersedia di dalam graf.

## 8. Cara Instalasi

Pastikan Python sudah terpasang di komputer dan VS Code dapat
menjalankan terminal.

Buka terminal pada folder utama proyek, kemudian jalankan:

```bash
python -m pip install -r requirements.txt
```

## 9. Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

```bash
python -m streamlit run app.py
```

Aplikasi akan dibuka melalui browser.

## 10. Cara Menggunakan Aplikasi

1. Pilih titik asal perjalanan.
2. Pilih titik tujuan perjalanan.
3. Amati lintasan dan panjang perjalanan awal.
4. Pilih ruas jalan yang akan dibalik arahnya.
5. Klik tombol **Balik arah**.
6. Bandingkan keterjangkauan dan panjang lintasan setelah perubahan.
7. Klik **Reset** untuk mengembalikan kondisi awal.

Panah menunjukkan arah jalan. Warna pada graf membedakan
simpul, lintasan, dan ruas yang mengalami perubahan.

## 11. Skenario Pengujian

### Skenario 1: Kondisi Awal

Pilih titik asal A dan tujuan L.

Amati apakah tujuan dapat dicapai dan catat lintasan serta
panjang lintasan yang diperoleh.

### Skenario 2: Pembalikan Arah Jalan

Balik arah ruas A menuju B, kemudian hitung ulang lintasan
dari A menuju L.

Bandingkan hasil dengan kondisi awal. Pada topologi demonstrasi,
pembalikan ruas A menuju B menjadi B menuju A menyebabkan
lintasan dari A menuju L tidak tersedia.

Hasil ini menunjukkan bahwa keterjangkauan dipengaruhi oleh
arah sisi, bukan hanya keberadaan hubungan antarsimpul.

## 12. Batasan Model

Model ini merupakan demonstrasi algoritma graf, bukan sistem
navigasi jalan nyata.

Model belum memperhitungkan:

- Kemacetan lalu lintas.
- Aturan belok di persimpangan.
- Penutupan jalan sementara.
- Kondisi geografis dan konektivitas jalan yang sebenarnya.
- Perubahan waktu tempuh.

## 13. Kesimpulan

One-Way City Explorer memperlihatkan bahwa arah sisi pada graf
berpengaruh terhadap keterjangkauan dan lintasan perjalanan.
Dengan membalik arah satu ruas jalan, lintasan yang sebelumnya
tersedia dapat berubah, menjadi lebih panjang, atau tidak lagi
tersedia.

Aplikasi ini juga menunjukkan pentingnya validasi lintasan
berdasarkan arah sisi serta interpretasi hasil sesuai dengan
batasan model yang digunakan.

