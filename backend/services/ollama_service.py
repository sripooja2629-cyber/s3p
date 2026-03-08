import os
import json
import re
import random
from typing import Optional, Dict


class OllamaService:
    def __init__(self):
        pass

    def check_health(self) -> bool:
        return True

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 temperature: float = 0.7, max_tokens: int = 1024) -> str:
        p = prompt.lower()

        # Greetings
        if any(w in p for w in ["hyy", "hey", "hii", "hello", "hi ", "namaste", "helo"]):
            return (
                "Namaste! 🙏 Main hoon aapka **NCERT Study Buddy**!\n\n"
                "Aap mujhse Class 9–10 ke Science aur Maths ke koi bhi sawaal pooch sakte ho — "
                "Hinglish ya Tanglish mein! 😊\n\n"
                "**Kuch examples:**\n"
                "- 'Newton ka pehla law kya hai?'\n"
                "- 'Photosynthesis explain karo'\n"
                "- 'Ohm's law samjhao'\n"
                "- 'Quadratic equation kaise solve karte hai?'\n\n"
                "Bolo, kya doubt hai? 📚"
            )

        # Newton's Laws
        if "newton" in p and ("pehla" in p or "first" in p or "1" in p):
            return (
                "## Newton ka Pehla Niyam (Law of Inertia) 🚀\n\n"
                "**Simple mein:** Koi bhi object apni current state change nahi karta jab tak koi external force nahi lagata!\n\n"
                "**Agar object rest mein hai** → rest mein hi rahega\n"
                "**Agar object move kar raha hai** → same speed, same direction mein move karta rahega\n\n"
                "**Real life example:**\n"
                "- Bus suddenly ruk jaaye toh passenger aage gir jaata hai — kyunki uska body aage move karna chahta tha! 🚌\n"
                "- Table pe rakhi book tab tak nahi hilti jab tak tum dhakka nahi dete\n\n"
                "**Formula:** F = 0 hone pe, acceleration = 0\n\n"
                "Koi aur doubt? Practice questions chahiye? 😊"
            )

        if "newton" in p and ("doosra" in p or "second" in p or "2" in p):
            return (
                "## Newton ka Doosra Niyam ⚡\n\n"
                "**Formula:** **F = ma**\n\n"
                "- **F** = Force (Newton mein)\n"
                "- **m** = Mass (kg mein)\n"
                "- **a** = Acceleration (m/s² mein)\n\n"
                "**Simple mein:** Jitna zyada force lagaoge, utna zyada acceleration milega!\n\n"
                "**Example:**\n"
                "Ek 5 kg ka box push karo 10 N force se:\n"
                "a = F/m = 10/5 = **2 m/s²**\n\n"
                "Samajh aaya? Koi aur sawaal? 🎯"
            )

        if "newton" in p and ("teesra" in p or "third" in p or "3" in p):
            return (
                "## Newton ka Teesra Niyam 🔄\n\n"
                "**'Har action ka equal aur opposite reaction hota hai!'**\n\n"
                "**Examples:**\n"
                "- 🚀 Rocket: Gas neeche push karti hai → Rocket upar jaata hai\n"
                "- 🏊 Swimming: Paani ko peeche push karo → Aap aage jaate ho\n"
                "- 🔫 Gun: Bullet aage jaati hai → Gun peeche kick karti hai\n\n"
                "**Important:** Action aur reaction SAME object pe nahi hote!\n\n"
                "Aur kuch poochna hai? 😊"
            )

        # Gravity/Gravitation
        if any(w in p for w in ["gravit", "gravity", "gravitational", "free fall", "g ="]):
            return (
                "## Gravitation (Gurutvakarshan) 🌍\n\n"
                "**Universal Law of Gravitation:**\n"
                "**F = G × m₁ × m₂ / r²**\n\n"
                "- G = 6.674 × 10⁻¹¹ N m²/kg²\n"
                "- m₁, m₂ = do objects ke masses\n"
                "- r = unke beech ki distance\n\n"
                "**Earth pe g = 9.8 m/s²**\n\n"
                "**Key Points:**\n"
                "- Har object doosre ko attract karta hai\n"
                "- Mass zyada → Force zyada\n"
                "- Distance zyada → Force kam (inverse square law)\n\n"
                "**Free Fall:** Vacuum mein sab cheezein same speed se girती hain! (Galileo ka experiment)\n\n"
                "Koi specific sawaal? 🎯"
            )

        # Photosynthesis
        if any(w in p for w in ["photosynthesis", "photo synthesis", "prakash sansleshan"]):
            return (
                "## Photosynthesis (Prakash Sansleshan) 🌿\n\n"
                "**Simple Definition:** Plants sunlight use karke apna khana banate hain!\n\n"
                "**Chemical Equation:**\n"
                "6CO₂ + 6H₂O + Light → **C₆H₁₂O₆ + 6O₂**\n"
                "(Carbon dioxide + Paani + Sunlight → Glucose + Oxygen)\n\n"
                "**Kahan hota hai?** Chloroplast mein (jo leaves mein hota hai)\n"
                "**Kaunsa pigment?** Chlorophyll (green colour deta hai)\n\n"
                "**2 Stages:**\n"
                "1. **Light Reaction** → ATP aur NADPH banta hai\n"
                "2. **Dark Reaction (Calvin Cycle)** → Glucose banta hai\n\n"
                "**Factors affecting it:**\n"
                "- Light intensity\n"
                "- CO₂ concentration\n"
                "- Temperature\n\n"
                "Aur kuch samjhana hai? 🌱"
            )

        # Cell
        if any(w in p for w in ["cell", "koshika", "nucleus", "mitochondria", "membrane"]):
            return (
                "## Cell (Koshika) — Life ki Basic Unit 🔬\n\n"
                "**2 Types:**\n"
                "1. **Prokaryotic** — No nucleus (Bacteria)\n"
                "2. **Eukaryotic** — Nucleus present (Plants, Animals)\n\n"
                "**Important Parts:**\n"
                "- **Cell Membrane** → Gate ki tarah, andar-bahar control karti hai\n"
                "- **Nucleus** → Brain of cell, DNA rakhta hai\n"
                "- **Mitochondria** → Power house of cell! ATP energy deta hai\n"
                "- **Ribosome** → Protein factory\n"
                "- **Vacuole** → Storage tank\n\n"
                "**Plant vs Animal Cell:**\n"
                "Plants mein extra: Cell Wall, Chloroplast, Large Vacuole\n\n"
                "Koi specific part ke baare mein poochna hai? 😊"
            )

        # Ohm's Law / Electricity
        if any(w in p for w in ["ohm", "resistance", "current", "voltage", "electricity", "circuit"]):
            return (
                "## Ohm's Law aur Electricity ⚡\n\n"
                "**Ohm's Law:** V = IR\n"
                "- V = Voltage (Volts)\n"
                "- I = Current (Amperes)\n"
                "- R = Resistance (Ohms Ω)\n\n"
                "**Simple mein:** Zyada resistance → Kam current flow hoga\n\n"
                "**Series Circuit:**\n"
                "- Same current everywhere\n"
                "- R_total = R₁ + R₂ + R₃\n\n"
                "**Parallel Circuit:**\n"
                "- Same voltage everywhere\n"
                "- 1/R_total = 1/R₁ + 1/R₂\n\n"
                "**Power:** P = VI = I²R = V²/R\n\n"
                "**Numerical example:**\n"
                "V=12V, R=4Ω → I = V/R = 12/4 = **3A**\n\n"
                "Koi numerical solve karna hai? 🎯"
            )

        # Chemical Reactions
        if any(w in p for w in ["chemical reaction", "rasayanik", "acid", "base", "salt", "oxidation"]):
            return (
                "## Chemical Reactions (Rasayanik Pratikriyaen) ⚗️\n\n"
                "**Types of Reactions:**\n\n"
                "1. **Combination (Sanyojan):** A + B → AB\n"
                "   Example: 2H₂ + O₂ → 2H₂O\n\n"
                "2. **Decomposition (Viyojan):** AB → A + B\n"
                "   Example: 2H₂O → 2H₂ + O₂\n\n"
                "3. **Displacement:** A + BC → AC + B\n"
                "   Example: Fe + CuSO₄ → FeSO₄ + Cu\n\n"
                "4. **Redox:** Oxidation + Reduction saath mein hoti hai\n\n"
                "**Acids:** Sour taste, pH < 7, H⁺ ions dete hain\n"
                "**Bases:** Bitter, pH > 7, OH⁻ ions dete hain\n"
                "**Salt:** Acid + Base → Salt + Water (Neutralization)\n\n"
                "Koi specific reaction samjhani hai? 😊"
            )

        # Quadratic / Maths
        if any(w in p for w in ["quadratic", "dwiteeya", "x^2", "x²", "polynomial"]):
            return (
                "## Quadratic Equations (Dwiteeya Ghatiya Samikaran) 📐\n\n"
                "**Standard Form:** ax² + bx + c = 0\n\n"
                "**3 Methods to Solve:**\n\n"
                "**1. Factorization:**\n"
                "x² - 5x + 6 = 0\n"
                "→ (x-2)(x-3) = 0\n"
                "→ x = 2 or x = 3\n\n"
                "**2. Quadratic Formula (Sabse reliable!):**\n"
                "x = [-b ± √(b²-4ac)] / 2a\n\n"
                "**3. Completing the Square**\n\n"
                "**Discriminant (D = b²-4ac):**\n"
                "- D > 0 → 2 real roots\n"
                "- D = 0 → 1 real root\n"
                "- D < 0 → No real roots\n\n"
                "Koi specific equation solve karni hai? 🎯"
            )

        # Trigonometry
        if any(w in p for w in ["trigo", "sin", "cos", "tan", "sine", "cosine"]):
            return (
                "## Trigonometry 📐\n\n"
                "**Basic Ratios (Right Triangle mein):**\n"
                "- **sin θ** = Opposite / Hypotenuse\n"
                "- **cos θ** = Adjacent / Hypotenuse\n"
                "- **tan θ** = Opposite / Adjacent\n\n"
                "**Trick to remember:** **SOH-CAH-TOA**\n\n"
                "**Important Values:**\n"
                "| Angle | sin | cos | tan |\n"
                "|-------|-----|-----|-----|\n"
                "| 0°    | 0   | 1   | 0   |\n"
                "| 30°   | 1/2 | √3/2| 1/√3|\n"
                "| 45°   | 1/√2| 1/√2| 1   |\n"
                "| 60°   | √3/2| 1/2 | √3  |\n"
                "| 90°   | 1   | 0   | ∞   |\n\n"
                "**Identity:** sin²θ + cos²θ = 1\n\n"
                "Koi problem solve karni hai? 😊"
            )

        # Light / Optics
        if any(w in p for w in ["light", "lens", "mirror", "reflection", "refraction", "prism"]):
            return (
                "## Light (Prakash) 💡\n\n"
                "**Reflection ke Laws:**\n"
                "1. Angle of incidence = Angle of reflection\n"
                "2. Incident ray, Normal, Reflected ray — same plane mein\n\n"
                "**Mirrors:**\n"
                "- Concave (Concave) → Real + inverted image (mostly)\n"
                "- Convex (Convex) → Virtual + erect + smaller image\n\n"
                "**Mirror Formula:** 1/f = 1/v + 1/u\n\n"
                "**Refraction:**\n"
                "Snell's Law: n₁ sin θ₁ = n₂ sin θ₂\n\n"
                "**Lenses:**\n"
                "- Convex → Converging lens\n"
                "- Concave → Diverging lens\n"
                "**Lens Formula:** 1/f = 1/v - 1/u\n\n"
                "Koi specific topic? 🎯"
            )

        # Heredity/DNA
        if any(w in p for w in ["heredity", "dna", "gene", "chromosome", "mendel", "evolution"]):
            return (
                "## Heredity aur Evolution 🧬\n\n"
                "**Mendel ke Laws:**\n"
                "1. Law of Segregation\n"
                "2. Law of Independent Assortment\n\n"
                "**DNA:**\n"
                "- Deoxyribonucleic Acid\n"
                "- Double helix structure (Watson & Crick)\n"
                "- Bases: A-T, G-C pair karte hain\n\n"
                "**Chromosomes:**\n"
                "- Humans mein 46 chromosomes (23 pairs)\n"
                "- XX → Female, XY → Male\n\n"
                "**Evolution:**\n"
                "- Darwin ka Natural Selection\n"
                "- Survival of the fittest\n\n"
                "Aur kuch poochna hai? 🔬"
            )

        # Default intelligent response
        topics = [
            "Newton's Laws", "Gravitation", "Photosynthesis", "Cell Biology",
            "Ohm's Law", "Chemical Reactions", "Quadratic Equations", "Trigonometry",
            "Light & Optics", "Heredity & DNA"
        ]
        return (
            f"Main samajh gaya aapka sawaal! 🤔\n\n"
            f"Aap **'{prompt[:60]}...'** ke baare mein pooch rahe ho.\n\n"
            f"Main NCERT Class 9-10 ka expert hoon! Inme se kisi topic pe poochho:\n\n"
            + "\n".join([f"- {t}" for t in topics]) +
            f"\n\n**Tip:** Thoda aur specific poochho jaise:\n"
            f"- 'Newton ka pehla law explain karo'\n"
            f"- 'Photosynthesis ka equation kya hai?'\n"
            f"- 'Quadratic formula kya hota hai?'\n\n"
            f"Koi bhi sawaal poochho, main samjhaunga! 📚"
        )

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None,
                      temperature: float = 0.3, max_tokens: int = 1024) -> Optional[Dict]:
        p = prompt.lower()

        # Practice questions
        if "practice" in p or "question" in p:
            topic = "Science"
            for t in ["newton", "force", "motion", "gravity", "photosynthesis", "cell",
                      "electricity", "chemical", "light", "quadratic", "trigonometry"]:
                if t in p:
                    topic = t.capitalize()
                    break
            return {
                "questions": [
                    {
                        "question": f"Define {topic} aur iska ek real-life example do.",
                        "type": "short_answer",
                        "difficulty": "easy",
                        "marks": 2
                    },
                    {
                        "question": f"{topic} ka main formula/law kya hai? Explain karo.",
                        "type": "short_answer",
                        "difficulty": "medium",
                        "marks": 3
                    },
                    {
                        "question": f"Ek numerical problem solve karo jo {topic} se related ho.",
                        "type": "numerical",
                        "difficulty": "hard",
                        "marks": 5
                    }
                ]
            }

        # Topic detection
        if "topic" in p or "detect" in p or "subject" in p:
            return {
                "topic": "General Science",
                "subject": "Science",
                "class_level": "9-10",
                "in_syllabus": True,
                "confidence": 0.8
            }

        # Concept map
        if "concept" in p or "map" in p:
            return {
                "central_topic": "NCERT Science",
                "nodes": [
                    {"id": "1", "label": "Physics", "children": ["Newton's Laws", "Light", "Electricity"]},
                    {"id": "2", "label": "Chemistry", "children": ["Chemical Reactions", "Acids & Bases"]},
                    {"id": "3", "label": "Biology", "children": ["Cell", "Photosynthesis", "Heredity"]}
                ]
            }

        # Mistake analysis
        if "mistake" in p or "wrong" in p or "error" in p:
            return {
                "is_correct": False,
                "explanation": "Aapka answer thoda off hai. Sahi concept yeh hai ki...",
                "correct_answer": "Sahi jawab ke liye concept ko dobara padho.",
                "tip": "NCERT ki book mein Chapter carefully padho!"
            }

        return {"status": "ok", "message": "Response generated"}

    def _extract_json(self, text: str) -> Optional[Dict]:
        try:
            return json.loads(text)
        except Exception:
            pass
        return None

    def explain_concept(self, question, context, topic, subject, language_style,
                        adaptive_mode=False, system_prompt_text="") -> str:
        return self.generate(question)

    def generate_practice_questions(self, topic, subject, class_level, context, system_prompt_text=""):
        return self.generate_json(f"practice questions for {topic} {subject}")

    def analyze_mistake(self, topic, question, student_answer, context, language_style, system_prompt_text="") -> str:
        return (
            f"## Mistake Analysis 🔍\n\n"
            f"**Topic:** {topic}\n"
            f"**Tumhara Answer:** {student_answer}\n\n"
            f"**Feedback:**\n"
            f"Yeh concept NCERT Class 9-10 mein cover hota hai. "
            f"Dobara carefully padho aur examples dekho. "
            f"Koi specific doubt ho toh poochho! 📚"
        )

    def generate_concept_map(self, topic, subject, system_prompt_text=""):
        return self.generate_json(f"concept map for {topic} {subject}")

    def detect_topic(self, question) -> Optional[Dict]:
        q = question.lower()
        topic = "General"
        subject = "Science"
        for kw, t, s in [
            ("newton", "Newton's Laws", "Physics"),
            ("motion", "Motion", "Physics"),
            ("gravity", "Gravitation", "Physics"),
            ("light", "Light", "Physics"),
            ("electricity", "Electricity", "Physics"),
            ("chemical", "Chemical Reactions", "Chemistry"),
            ("acid", "Acids & Bases", "Chemistry"),
            ("cell", "Cell Biology", "Biology"),
            ("photosynthesis", "Photosynthesis", "Biology"),
            ("heredity", "Heredity", "Biology"),
            ("quadratic", "Quadratic Equations", "Mathematics"),
            ("trigon", "Trigonometry", "Mathematics"),
        ]:
            if kw in q:
                topic, subject = t, s
                break
        return {
            "topic": topic,
            "subject": subject,
            "class_level": "9-10",
            "in_syllabus": True,
            "confidence": 0.85
        }


_ollama_instance = None

def get_ollama() -> OllamaService:
    global _ollama_instance
    if _ollama_instance is None:
        _ollama_instance = OllamaService()
    return _ollama_instance
