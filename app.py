
from pathlib import Path

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st


# ==================================================
# 1. KONFIGURASI APLIKASI
# ==================================================

st.set_page_config(
    page_title="One-Way City Explorer",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 One-Way City Explorer")
st.subheader("Balik arah satu jalan dan lihat perubahan rute")

st.write(
    "Aplikasi ini menunjukkan bagaimana arah jalan memengaruhi "
    "keterjangkauan dan panjang lintasan perjalanan."
)

st.info(
    "Model demonstrasi: konektivitas 12 simpul disimulasikan. "
    "Atribut ruas diambil dari road_network.csv. "
    "Jaringan ini bukan representasi konektivitas jalan nyata."
)


# ==================================================
# 2. MEMBACA DATASET
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

kemungkinan_file = [
    BASE_DIR / "road_network.csv",
    BASE_DIR / "data" / "road_network_international.csv",
    BASE_DIR / "data" / "road_network.csv",
]

CSV_PATH = next(
    (p for p in kemungkinan_file if p.exists()),
    None
)

if CSV_PATH is None:
    st.error(
        "File dataset tidak ditemukan. Pastikan file berada "
        "di folder data dengan nama road_network.csv."
    )
    st.stop()

df = pd.read_csv(CSV_PATH)

kolom_wajib = [
    "road_id",
    "road_name",
    "length_km"
]

if not all(k in df.columns for k in kolom_wajib):
    st.error(
        "Kolom road_id, road_name, dan length_km "
        "harus tersedia dalam dataset."
    )
    st.stop()

df["length_km"] = pd.to_numeric(
    df["length_km"], errors="coerce"
)

df = df.dropna(subset=["length_km"])
df = df[df["length_km"] > 0].reset_index(drop=True)

if len(df) < 17:
    st.error("Dataset memerlukan minimal 17 ruas dengan panjang valid.")
    st.stop()


# ==================================================
# 3. MEMBANGUN MODEL GRAF DEMONSTRASI
# ==================================================

simpul = list("ABCDEFGHIJKL")

# Setiap pasangan adalah arah awal sebuah ruas.
# Topologi ini merupakan simulasi, bukan hasil
# rekonstruksi hubungan geografis dari CSV.

struktur_jalan = [
    ("A", "B"),
    ("B", "C"),
    ("C", "D"),
    ("D", "E"),
    ("E", "F"),
    ("F", "G"),
    ("G", "H"),
    ("H", "I"),
    ("I", "J"),
    ("J", "K"),
    ("K", "L"),
    ("B", "E"),
    ("F", "C"),
    ("F", "J"),
    ("L", "H"),
    ("D", "H"),
    ("J", "G"),
]

G_awal = nx.DiGraph()
G_awal.add_nodes_from(simpul)

data_ruas = {}

for i, (asal, tujuan) in enumerate(struktur_jalan):
    row = df.iloc[i]

    atribut = {
        "road_id": str(row["road_id"]),
        "road_name": str(row["road_name"]),
        "length_km": float(row["length_km"]),
        "flipped": False,
    }

    G_awal.add_edge(asal, tujuan, **atribut)
    data_ruas[str(row["road_id"])] = (asal, tujuan)

# Posisi simpul dibuat tetap agar mudah dibandingkan.
pos = nx.circular_layout(G_awal)


# ==================================================
# 4. FUNGSI MEMBALIK ARAH JALAN
# ==================================================

def buat_graf(flipped_road_id=None):
    G = G_awal.copy()

    if flipped_road_id is not None:
        for asal, tujuan, atribut in list(G.edges(data=True)):
            if atribut["road_id"] == flipped_road_id:
                atribut_baru = atribut.copy()

                G.remove_edge(asal, tujuan)
                atribut_baru["flipped"] = True

                G.add_edge(
                    tujuan,
                    asal,
                    **atribut_baru
                )
                break

    return G


# ==================================================
# 5. MENCARI DAN MEMVALIDASI LINTASAN
# ==================================================

def cari_lintasan(G, asal, tujuan):
    if not nx.has_path(G, asal, tujuan):
        return None, None

    lintasan = nx.shortest_path(
        G,
        source=asal,
        target=tujuan,
        weight="length_km"
    )

    # Validasi: setiap langkah harus mengikuti
    # arah sisi yang benar-benar tersedia.
    valid = all(
        G.has_edge(u, v)
        for u, v in zip(lintasan[:-1], lintasan[1:])
    )

    if not valid:
        raise ValueError("Validasi lintasan gagal.")

    total_km = sum(
        G[u][v]["length_km"]
        for u, v in zip(lintasan[:-1], lintasan[1:])
    )

    return lintasan, total_km


# ==================================================
# 6. FUNGSI VISUALISASI GRAF
# ==================================================

def gambar_graf(G, asal, tujuan, lintasan, judul):
    fig, ax = plt.subplots(figsize=(8, 6))

    sisi_lintasan = set()

    if lintasan:
        sisi_lintasan = set(
            zip(lintasan[:-1], lintasan[1:])
        )

    warna_sisi = []

    for u, v, atribut in G.edges(data=True):
        if (u, v) in sisi_lintasan:
            warna_sisi.append("#16A34A")
        elif atribut.get("flipped", False):
            warna_sisi.append("#EA580C")
        else:
            warna_sisi.append("#AAB4C3")

    warna_simpul = []

    for n in G.nodes():
        if n == asal:
            warna_simpul.append("#22C55E")
        elif n == tujuan:
            warna_simpul.append("#F59E0B")
        else:
            warna_simpul.append("#93C5FD")

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=warna_simpul,
        node_size=850,
        edgecolors="#334155",
        linewidths=1.2,
        ax=ax
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=11,
        font_weight="bold",
        ax=ax
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=list(G.edges()),
        edge_color=warna_sisi,
        width=2.2,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=19,
        connectionstyle="arc3,rad=0.08",
        min_source_margin=15,
        min_target_margin=18,
        ax=ax
    )

    label_sisi = {
        (u, v): f"{atribut['length_km']:.1f}"
        for u, v, atribut in G.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=label_sisi,
        font_size=7,
        rotate=False,
        label_pos=0.5,
        ax=ax
    )

    ax.set_title(judul, fontsize=12, fontweight="bold")
    ax.axis("off")

    fig.tight_layout()
    return fig


# ==================================================
# 7. KONTROL INTERAKTIF
# ==================================================

st.sidebar.header("🎛️ Kontrol perjalanan")

asal = st.sidebar.selectbox(
    "Pilih titik asal",
    simpul,
    index=0
)

tujuan = st.sidebar.selectbox(
    "Pilih titik tujuan",
    simpul,
    index=11
)

st.sidebar.divider()
st.sidebar.subheader("🔄 Ubah arah jalan")

pilihan_ruas = {}

for u, v in struktur_jalan:
    atribut = G_awal[u][v]
    road_id = atribut["road_id"]

    label = (
        f"{u} → {v} | {road_id} | "
        f"{atribut['road_name']}"
    )

    pilihan_ruas[label] = road_id

label_pilihan = st.sidebar.selectbox(
    "Pilih ruas yang ingin dibalik",
    list(pilihan_ruas.keys())
)

road_id_pilihan = pilihan_ruas[label_pilihan]

if "flipped_road_id" not in st.session_state:
    st.session_state.flipped_road_id = None

col_tombol1, col_tombol2 = st.sidebar.columns(2)

with col_tombol1:
    if st.button("Balik arah", use_container_width=True):
        st.session_state.flipped_road_id = road_id_pilihan

with col_tombol2:
    if st.button("Reset", use_container_width=True):
        st.session_state.flipped_road_id = None

st.sidebar.caption(
    "Balik arah mengubah satu ruas pada model. "
    "Reset mengembalikan graf ke kondisi awal."
)


# ==================================================
# 8. HITUNG KONDISI AWAL DAN SESUDAH PERUBAHAN
# ==================================================

G_sekarang = buat_graf(st.session_state.flipped_road_id)

path_awal, jarak_awal = cari_lintasan(
    G_awal, asal, tujuan
)

path_sekarang, jarak_sekarang = cari_lintasan(
    G_sekarang, asal, tujuan
)


# ==================================================
# 9. RINGKASAN HASIL
# ==================================================

st.header("📊 Perbandingan hasil")

m1, m2, m3 = st.columns(3)

m1.metric(
    "Simpul",
    G_sekarang.number_of_nodes()
)

m2.metric(
    "Ruas berarah",
    G_sekarang.number_of_edges()
)

if st.session_state.flipped_road_id is None:
    status = "Kondisi awal"
else:
    status = "Satu ruas dibalik"

m3.metric("Status jaringan", status)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Sebelum perubahan")

    if path_awal is None:
        st.error(f"Tidak ada lintasan {asal} → {tujuan}.")
    else:
        st.success("Lintasan tersedia")
        st.write("Lintasan:", " → ".join(path_awal))
        st.write(f"Panjang lintasan: {jarak_awal:.2f} km")

with c2:
    st.subheader("Sesudah perubahan")

    if path_sekarang is None:
        st.error(f"Tidak ada lintasan {asal} → {tujuan}.")
    else:
        st.success("Lintasan tersedia")
        st.write("Lintasan:", " → ".join(path_sekarang))
        st.write(
            f"Panjang lintasan: {jarak_sekarang:.2f} km"
        )

if path_awal is not None and path_sekarang is not None:
    selisih = jarak_sekarang - jarak_awal

    if abs(selisih) < 1e-9:
        st.info("Panjang lintasan terpendek tidak berubah.")
    elif selisih > 0:
        st.warning(
            f"Lintasan terpendek bertambah {selisih:.2f} km."
        )
    else:
        st.info(
            f"Lintasan terpendek berkurang {abs(selisih):.2f} km."
        )

elif path_awal is not None and path_sekarang is None:
    st.warning(
        "Tujuan dapat dicapai sebelum perubahan, "
        "tetapi tidak dapat dicapai setelah arah jalan dibalik."
    )

elif path_awal is None and path_sekarang is not None:
    st.info(
        "Pembalikan arah membuat tujuan yang sebelumnya "
        "tidak terjangkau menjadi dapat dicapai."
    )

else:
    st.warning(
        "Tidak ada lintasan pada kedua kondisi. "
        "Coba pilih asal dan tujuan yang berbeda."
    )


# ==================================================
# 10. VISUALISASI SEBELUM DAN SESUDAH
# ==================================================

st.header("🗺️ Visualisasi jaringan")

st.markdown(
    """
    **Legenda:**
    - 🟢 Simpul asal dan lintasan yang dipilih
    - 🟠 Ruas yang arahnya dibalik
    - 🔵 Simpul lainnya
    - Panah menunjukkan arah perjalanan
    - Angka pada sisi menunjukkan panjang ruas (km)
    """
)

v1, v2 = st.columns(2)

with v1:
    fig_awal = gambar_graf(
        G_awal,
        asal,
        tujuan,
        path_awal,
        "Kondisi awal"
    )
    st.pyplot(fig_awal)
    plt.close(fig_awal)

with v2:
    fig_sekarang = gambar_graf(
        G_sekarang,
        asal,
        tujuan,
        path_sekarang,
        "Kondisi setelah perubahan"
    )
    st.pyplot(fig_sekarang)
    plt.close(fig_sekarang)


# ==================================================
# 11. VALIDASI DAN INTERPRETASI
# ==================================================

st.header("🔎 Validasi komputasi")

if path_sekarang is not None:
    validasi = all(
        G_sekarang.has_edge(u, v)
        for u, v in zip(
            path_sekarang[:-1],
            path_sekarang[1:]
        )
    )

    st.write("Lintasan mengikuti arah sisi:", validasi)
    st.write(
        "Validasi keterjangkauan NetworkX:",
        nx.has_path(G_sekarang, asal, tujuan)
    )
else:
    st.write("Lintasan tidak tersedia untuk pasangan titik ini.")

if st.session_state.flipped_road_id is not None:
    st.write(
        "ID ruas yang dibalik:",
        st.session_state.flipped_road_id
    )

    for u, v, atribut in G_sekarang.edges(data=True):
        if atribut.get("flipped", False):
            st.write(f"Arah baru: {u} → {v}")
            break

st.caption(
    "Batas interpretasi: panjang lintasan merupakan jumlah atribut "
    "length_km dari ruas yang digunakan. Model tidak memasukkan "
    "kemacetan, aturan belok, penutupan jalan, atau kondisi geografis "
    "nyata. Struktur koneksi dan arah awal merupakan simulasi."
)
