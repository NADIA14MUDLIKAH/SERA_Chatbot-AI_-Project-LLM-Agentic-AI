import sys
from src.chatbot import SeraChatbot

def main():
    print("=" * 50)
    print(" 🌱 SERA - Sistem Edukasi & Rekomendasi Agrikultur")
    print("=" * 50)
    print("Ketik keluhan tanamanmu di bawah ini.")
    print("Perintah khusus:")
    print(" - 'exit'  : Keluar aplikasi")
    print(" - 'clear' : Reset percakapan")
    print(" - 'save'  : Simpan percakapan ke JSON\n")

    bot = SeraChatbot()

    while True:
        try:
            user_input = input("\n🧑‍🌾 Petani : ").strip()
        except KeyboardInterrupt:
            print("\nKeluar aplikasi...")
            break

        if not user_input:
            continue

        command = user_input.lower()
        if command == "exit":
            print("Terima kasih telah menggunakan SERA. Sampai jumpa!")
            break
        elif command == "clear":
            bot.reset()
            print("✅ Riwayat percakapan telah dibersihkan.")
            continue
        elif command == "save":
            filepath = bot.save()
            print(f"💾 Percakapan berhasil disimpan di: {filepath}")
            continue

        print("🤖 SERA   : ", end="", flush=True)
        for chunk in bot.chat_stream(user_input):
            print(chunk, end="", flush=True)
        print() 

if __name__ == "__main__":
    main()