import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Lokasi default: <folder proyek>/data/knowledge_base.json
# (dihitung dari lokasi file ini, jadi aman walau aplikasi dijalankan dari folder lain)
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

KnowledgeBase = Union[List[Dict[str, Any]], Dict[str, Any]]

# Kata umum yang tidak membantu mencocokkan gejala
STOPWORDS = {
    "yang", "dan", "dari", "dengan", "untuk", "pada", "adalah", "ini", "itu",
    "aku", "saya", "kamu", "anda", "nih", "dong", "sih", "deh", "kok", "yaaa",
    "tidak", "gak", "nggak", "enggak", "udah", "sudah", "belum", "baru", "masih",
    "juga", "atau", "tapi", "karena", "kalau", "kalo", "agar", "supaya", "apa",
    "apakah", "kenapa", "bagaimana", "gimana", "mengapa", "banyak", "sedikit",
    "sangat", "sekali", "lagi", "padahal", "seperti", "terus", "habis", "sejak",
    "kemarin", "sekarang", "tanam", "tanem", "tanaman", "daun", "gejala",
    "muncul", "terlihat", "tampak", "adanya", "bisa", "mau", "tolong", "masalah",
    "kayak", "kayaknya", "tiba", "bagian", "sudah", "belakangan",
}


# ----------------------------------------------------------------------
# Memuat data
# ----------------------------------------------------------------------
def load_knowledge_base(filepath: Union[str, Path] = DEFAULT_KB_PATH) -> KnowledgeBase:
    path = Path(filepath)
    if not path.exists():
        return {"error": "File knowledge base tidak ditemukan."}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _sebagai_daftar(kb_data: KnowledgeBase) -> List[Dict[str, Any]]:
    """Seragamkan: daftar tanaman (baru) atau satu objek (lama) -> list."""
    if isinstance(kb_data, dict):
        if "error" in kb_data:
            return []
        return [kb_data]
    return list(kb_data or [])


def _apakah_umum(nama_tanaman: str) -> bool:
    return nama_tanaman.lower().startswith("umum")


# ----------------------------------------------------------------------
# Utilitas pencocokan teks
# ----------------------------------------------------------------------
def _normalisasi(teks: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", teks.lower())


def _kata_penting(teks: str) -> set:
    hasil = set()
    for kata in _normalisasi(teks).split():
        if len(kata) > 6 and kata.endswith("nya"):
            kata = kata[:-3]
        if len(kata) >= 4 and kata not in STOPWORDS:
            hasil.add(kata)
    return hasil


def deteksi_tanaman(kb_data: KnowledgeBase, teks: str) -> List[str]:
    """Cari nama tanaman (termasuk alias, mis. 'cabe', 'lombok') di dalam teks."""
    teks_n = " " + _normalisasi(teks) + " "
    ditemukan = []
    for entri in _sebagai_daftar(kb_data):
        nama = entri.get("tanaman", "")
        if not nama or _apakah_umum(nama):
            continue
        kunci = [nama.lower()] + [a.lower() for a in entri.get("alias", [])]
        pola = "|".join(re.escape(k) for k in kunci)
        if re.search(rf"\b(?:{pola})(?:nya|ku|mu)?\b", teks_n):
            ditemukan.append(nama)
    return ditemukan


def _skor_kasus(kasus: Dict[str, Any], teks_n: str, kata_teks: set) -> int:
    skor = 0
    frasa = [kasus.get("gejala_utama", "")] + list(kasus.get("sinonim_gejala", []))
    for f in frasa:
        f_n = _normalisasi(f).strip()
        if f_n and f_n in teks_n:
            skor += 3

    teks_kasus = " ".join(
        [kasus.get("gejala_utama", ""), " ".join(kasus.get("sinonim_gejala", [])), kasus.get("kondisi", "")]
    )
    skor += len(_kata_penting(teks_kasus) & kata_teks)
    return skor


# ----------------------------------------------------------------------
# Format teks untuk prompt
# ----------------------------------------------------------------------
def _gabung(nilai: Any, pemisah: str = " | ") -> str:
    if isinstance(nilai, list):
        return pemisah.join(str(x) for x in nilai)
    return str(nilai) if nilai else ""


def _format_kasus(nama_tanaman: str, kasus: Dict[str, Any]) -> str:
    baris = [f"[Data: {nama_tanaman}]", f"Gejala: {kasus.get('gejala_utama', '')}"]
    if kasus.get("pertanyaan_lanjutan"):
        baris.append(f"Tanyakan: {_gabung(kasus['pertanyaan_lanjutan'])}")
    baris.append(f"Kondisi: {kasus.get('kondisi', '')}")
    baris.append(f"Kemungkinan: {kasus.get('kemungkinan', '')}")
    if kasus.get("ciri_pembeda"):
        baris.append(f"Ciri pembeda: {kasus['ciri_pembeda']}")
    if kasus.get("saran"):
        baris.append(f"Saran: {_gabung(kasus['saran'])}")
    if kasus.get("pencegahan"):
        baris.append(f"Pencegahan: {_gabung(kasus['pencegahan'])}")
    if kasus.get("urgensi"):
        baris.append(f"Urgensi: {kasus['urgensi']}")
    return "\n".join(baris)


def pilih_konteks_relevan(
    kb_data: KnowledgeBase,
    teks_gejala: str,
    tanaman_aktif: Optional[List[str]] = None,
    max_kasus: int = 4,
) -> str:
    """Ambil hanya kasus yang paling cocok dengan percakapan (hemat token).

    - Jika tanaman sudah disebut: ambil kasus tanaman itu yang cocok dengan gejala.
    - Jika belum ada yang cocok: beri daftar gejala yang tercatat sebagai petunjuk pertanyaan.
    - Jika tanaman tidak punya data khusus: pakai kasus 'Umum'.
    """
    kb = _sebagai_daftar(kb_data)
    if not kb:
        return ""

    aktif = list(tanaman_aktif or [])
    for t in deteksi_tanaman(kb, teks_gejala):
        if t not in aktif:
            aktif.append(t)

    teks_n = " " + _normalisasi(teks_gejala) + " "
    kata_teks = _kata_penting(teks_gejala)

    khusus, umum = [], []
    for entri in kb:
        nama = entri.get("tanaman", "")
        for kasus in entri.get("kasus", []):
            skor = _skor_kasus(kasus, teks_n, kata_teks)
            if skor <= 0:
                continue
            if _apakah_umum(nama):
                umum.append((skor, nama, kasus))
            elif nama in aktif:
                khusus.append((skor, nama, kasus))

    khusus.sort(key=lambda x: -x[0])
    umum.sort(key=lambda x: -x[0])

    terpilih = khusus[:max_kasus]
    if not terpilih:
        terpilih = umum[:3]

    tersedia = [e.get("tanaman", "") for e in kb if not _apakah_umum(e.get("tanaman", ""))]
    bagian = [f"Tanaman dengan data khusus: {', '.join(tersedia)}. Tanaman lain memakai panduan umum."]
    if aktif:
        bagian.append(f"Tanaman yang sedang dibahas: {', '.join(aktif)}")

    # Belum ada kasus khusus yang cocok -> beri petunjuk daftar gejala tanaman tsb
    if aktif and not khusus:
        for entri in kb:
            if entri.get("tanaman") in aktif:
                gejala = []
                for k in entri.get("kasus", []):
                    g = k.get("gejala_utama", "")
                    if g and g not in gejala:
                        gejala.append(g)
                bagian.append(f"Gejala yang tercatat untuk {entri['tanaman']}: {'; '.join(gejala)}")

    if not terpilih:
        bagian.append("Belum ada kasus yang cocok dengan percakapan. Tanyakan jenis tanaman dan gejalanya.")

    for _, nama, kasus in terpilih:
        bagian.append(_format_kasus(nama, kasus))

    return "\n\n".join(bagian)


def format_knowledge_base_for_prompt(kb_data: KnowledgeBase) -> str:
    """Versi lengkap (SEMUA kasus). Besar, jadi jangan dipakai untuk prompt
    di model dengan batas token kecil. Disimpan untuk kompatibilitas/debug."""
    blok = []
    for entri in _sebagai_daftar(kb_data):
        baris = [f"=== Tanaman: {entri.get('tanaman', 'Umum')} ==="]
        for kasus in entri.get("kasus", []):
            baris.append(_format_kasus(entri.get("tanaman", "Umum"), kasus))
            baris.append("")
        blok.append("\n".join(baris))
    return "\n".join(blok).strip()