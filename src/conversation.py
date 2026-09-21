from typing import List, Dict
from src.prompts import get_system_prompt
from src.knowledge_base import (
    load_knowledge_base,
    pilih_konteks_relevan,
    deteksi_tanaman,
)

# Jumlah pesan terakhir (user + asisten) yang dikirim ke model.
# Makin kecil = makin hemat token.
MAX_RIWAYAT = 6

# Jumlah pesan pengguna terakhir yang dipakai untuk mencocokkan gejala.
JENDELA_GEJALA = 6


class ConversationManager:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.kb_data = None
        self.pesan_pengguna: List[str] = []
        self.tanaman_aktif: List[str] = []
        self.reset_history()

    def reset_history(self):
        self.kb_data = load_knowledge_base()
        self.pesan_pengguna = []
        self.tanaman_aktif = []
        self.messages = [
            {"role": "system", "content": self._susun_system_prompt()}
        ]

    def _susun_system_prompt(self) -> str:
        """Bangun system prompt dengan hanya kasus yang relevan (hemat token)."""
        teks_gejala = " ".join(self.pesan_pengguna[-JENDELA_GEJALA:])
        kb_context = pilih_konteks_relevan(
            self.kb_data, teks_gejala, tanaman_aktif=self.tanaman_aktif
        )
        return get_system_prompt(kb_context)

    def add_user_message(self, content: str):
        self.pesan_pengguna.append(content)

        # Ingat tanaman yang terakhir disebut (walau nanti sudah di luar jendela gejala)
        baru = deteksi_tanaman(self.kb_data, content)
        if baru:
            self.tanaman_aktif = baru

        # Perbarui system prompt sesuai isi percakapan terbaru
        self.messages[0]["content"] = self._susun_system_prompt()
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        """System prompt + riwayat terbaru saja."""
        sistem = self.messages[0]
        riwayat = self.messages[1:][-MAX_RIWAYAT:]
        # Pastikan riwayat dimulai dari pesan pengguna
        while riwayat and riwayat[0]["role"] != "user":
            riwayat = riwayat[1:]
        return [sistem] + riwayat

    def get_full_history(self) -> List[Dict[str, str]]:
        """Seluruh riwayat percakapan (tanpa dipotong), untuk disimpan ke file."""
        return self.messages

    def batalkan_pesan_terakhir(self):
        """Hapus pesan pengguna terakhir, dipakai bila permintaan ke API gagal
        supaya pesan yang gagal tidak menumpuk di riwayat."""
        if len(self.messages) > 1 and self.messages[-1]["role"] == "user":
            self.messages.pop()
            if self.pesan_pengguna:
                self.pesan_pengguna.pop()

            # Hitung ulang tanaman aktif dari pesan yang tersisa
            self.tanaman_aktif = []
            for teks in self.pesan_pengguna:
                baru = deteksi_tanaman(self.kb_data, teks)
                if baru:
                    self.tanaman_aktif = baru

            self.messages[0]["content"] = self._susun_system_prompt()