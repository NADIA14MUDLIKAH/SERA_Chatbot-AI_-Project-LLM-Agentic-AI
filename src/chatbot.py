from src.conversation import ConversationManager
from src.llm_client import get_chat_response_stream
from src.commands import save_history_to_file

# Awalan pesan galat yang dikembalikan llm_client saat API gagal
PREFIX_GALAT = "[Sistem]"


class SeraChatbot:
    def __init__(self):
        self.conv_manager = ConversationManager()

    def chat_stream(self, user_input: str):
        self.conv_manager.add_user_message(user_input)

        messages = self.conv_manager.get_messages()
        stream_response = get_chat_response_stream(messages)

        full_response = ""
        for chunk in stream_response:
            full_response += chunk
            yield chunk

        # Jika API gagal, jangan simpan pesan galat sebagai jawaban asisten
        # dan batalkan pesan pengguna yang gagal supaya bisa dikirim ulang.
        if full_response.strip().startswith(PREFIX_GALAT):
            self.conv_manager.batalkan_pesan_terakhir()
            return

        self.conv_manager.add_assistant_message(full_response)

    def reset(self):
        self.conv_manager.reset_history()

    def save(self) -> str:
        # Simpan riwayat LENGKAP, bukan versi yang dipotong untuk dikirim ke model
        return save_history_to_file(self.conv_manager.get_full_history())