import unittest
import sys
from pathlib import Path

# Menambahkan direktori root ke path agar bisa import file dari folder src
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.knowledge_base import load_knowledge_base
from src.conversation import ConversationManager

class TestSeraChatbot(unittest.TestCase):
    
    def test_1_knowledge_base_loading(self):
        """Test apakah file knowledge_base.json berhasil dimuat dengan benar."""
        kb_data = load_knowledge_base()
        
        # Harus mengembalikan dictionary/JSON, bukan error
        self.assertIsInstance(kb_data, dict)
        self.assertNotIn("error", kb_data, "Gagal memuat knowledge base, pastikan file JSON ada.")
        self.assertEqual(kb_data.get("tanaman"), "Cabai")

    def test_2_conversation_initialization(self):
        """Test apakah history percakapan diinisialisasi dengan system prompt yang baru."""
        manager = ConversationManager()
        messages = manager.get_messages()
        
        # Minimal harus ada 1 pesan yaitu system prompt
        self.assertTrue(len(messages) > 0)
        self.assertEqual(messages[0]["role"], "system")
        
        # Memastikan prompt menggunakan struktur yang sudah kita perbarui (ada label [ROLE])
        self.assertIn("[ROLE]", messages[0]["content"]) 

    def test_3_add_user_message(self):
        """Test apakah keluhan petani berhasil ditambahkan ke riwayat (history)."""
        manager = ConversationManager()
        initial_length = len(manager.get_messages())
        
        keluhan_petani = "Daun cabai saya menguning dan keriting"
        manager.add_user_message(keluhan_petani)
        
        messages = manager.get_messages()
        
        # Jumlah pesan harus bertambah 1
        self.assertEqual(len(messages), initial_length + 1)
        self.assertEqual(messages[-1]["role"], "user")
        self.assertEqual(messages[-1]["content"], keluhan_petani)

if __name__ == "__main__":
    unittest.main()