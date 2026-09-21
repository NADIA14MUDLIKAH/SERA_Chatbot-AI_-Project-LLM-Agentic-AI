from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, TOP_P

client = Groq(api_key=GROQ_API_KEY)

def get_chat_response_stream(messages: list):
    """Mengirim pesan ke Groq API dan mengembalikan generator untuk efek streaming."""
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"\n[Sistem] Maaf, terjadi kesalahan pada API: {str(e)}"