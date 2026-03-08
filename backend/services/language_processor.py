import re
from typing import Tuple

HINGLISH_MAP = {
    "kya": "what", "kaise": "how", "kyun": "why", "bhai": "", "yaar": "",
    "hai": "is", "hota": "happens", "bata": "explain", "samajh": "understand",
    "nahi": "not", "matlab": "meaning", "batao": "tell", "samjhao": "explain",
}

TANGLISH_MAP = {
    "enna": "what", "epdi": "how", "yen": "why", "da": "", "di": "", "anna": "", "akka": "",
    "sollu": "explain", "puriyala": "don't understand", "theriyathu": "don't know",
}

SCIENCE_KEYWORDS = {
    "physics": ["motion", "force", "gravity", "light", "sound", "electricity", "magnetism",
                "work", "energy", "power", "pressure", "velocity", "acceleration", "newton",
                "ohm", "current", "voltage", "gati", "bal", "prakash", "bijli", "urja"],
    "chemistry": ["atom", "molecule", "element", "compound", "reaction", "acid", "base",
                  "salt", "carbon", "metal", "non-metal", "periodic table", "bond",
                  "solution", "parmanu", "tatva"],
    "biology": ["cell", "tissue", "organ", "photosynthesis", "respiration", "nutrition",
                "reproduction", "heredity", "evolution", "nervous system", "ecosystem",
                "koshika", "poshan", "uyirmiyam"],
    "mathematics": ["algebra", "geometry", "trigonometry", "statistics", "polynomial",
                    "quadratic", "triangle", "circle", "probability", "surface area",
                    "volume", "coordinate", "beejganit"],
}


def detect_language_style(text: str) -> str:
    text_lower = text.lower()
    hindi_markers = ["kya", "kaise", "kyun", "bhai", "yaar", "hai", "hota", "matlab",
                     "samajh", "batao", "accha", "theek", "nahi", "mujhe", "mera"]
    tamil_markers = ["enna", "epdi", "yen", "da", "di", "anna", "akka", "sollu",
                     "puriyala", "theriyuma", "theriyathu", "padikanum", "vanakkam"]
    hindi_count = sum(1 for w in hindi_markers if w in text_lower)
    tamil_count = sum(1 for w in tamil_markers if w in text_lower)
    if tamil_count > hindi_count and tamil_count > 0:
        return "tanglish"
    elif hindi_count > 0:
        return "hinglish"
    return "english"


def detect_subject(text: str) -> str:
    text_lower = text.lower()
    scores = {subj: sum(1 for kw in kws if kw in text_lower) for subj, kws in SCIENCE_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


def normalize_query(text: str) -> Tuple[str, str, str]:
    lang_style = detect_language_style(text)
    subject = detect_subject(text)
    cleaned = re.sub(r'\s+', ' ', text).strip()
    cleaned = re.sub(r'[^\w\s\?\!\.\,\-\']', ' ', cleaned)
    return cleaned.strip(), lang_style, subject


def check_out_of_syllabus_keywords(text: str) -> bool:
    out_of_scope = [
        "class 11", "class 12", "jee", "neet", "iit", "competitive exam",
        "current affairs", "gk", "history", "geography", "political science",
        "economics", "english literature", "computer science", "coding",
        "programming", "stock market", "cryptocurrency", "sports news",
        "bollywood", "cricket score", "weather", "cooking recipe"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in out_of_scope)
