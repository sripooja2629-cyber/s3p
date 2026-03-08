import os
import re
import hashlib
from pathlib import Path
from typing import Optional

TTS_OUTPUT_DIR = os.getenv("TTS_OUTPUT_DIR", "./tts_output")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)


def clean_text_for_tts(text: str) -> str:
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'^\s*[-*•]\s', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def get_audio_cache_path(text: str) -> str:
    text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
    return os.path.join(TTS_OUTPUT_DIR, f"audio_{text_hash}.wav")


def generate_audio_gtts(text: str, output_path: str):
    try:
        from gtts import gTTS
        mp3_path = output_path.replace('.wav', '.mp3')
        gTTS(text=text, lang='en', slow=False).save(mp3_path)
        return True, mp3_path
    except Exception as e:
        print(f"⚠️ gTTS error: {e}")
        return False, None


def generate_tts(text: str) -> Optional[str]:
    clean = clean_text_for_tts(text)
    if not clean:
        return None
    if len(clean) > 500:
        clean = clean[:500] + "."
    cache_path = get_audio_cache_path(clean)
    mp3_cache_path = cache_path.replace('.wav', '.mp3')
    if os.path.exists(cache_path):
        return cache_path
    if os.path.exists(mp3_cache_path):
        return mp3_cache_path
    success, mp3_path = generate_audio_gtts(clean, cache_path)
    if success and mp3_path:
        return mp3_path
    print("❌ TTS generation failed. Install: pip install gtts")
    return None


def get_tts_status() -> dict:
    status = {"coqui": False, "gtts": False}
    try:
        import TTS; status["coqui"] = True
    except ImportError:
        pass
    try:
        import gtts; status["gtts"] = True
    except ImportError:
        pass
    return status
