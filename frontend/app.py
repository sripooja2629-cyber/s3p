"""
NCERT Hinglish/Tanglish Chatbot — Streamlit Frontend
Student chat UI + Teacher Analytics Dashboard
"""
import streamlit as st
import requests
import uuid
import os

API_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(page_title="NCERT Study Buddy", page_icon="📚",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp { background-color: #f0f4ff; }
.user-bubble { background: linear-gradient(135deg,#667eea,#764ba2);color:white;padding:12px 18px;border-radius:18px 18px 4px 18px;margin:8px 0 8px 20%;display:block;font-size:15px;line-height:1.5;box-shadow:0 2px 8px rgba(102,126,234,0.3); }
.ai-bubble { background:white;color:#2d3748;padding:14px 18px;border-radius:18px 18px 18px 4px;margin:8px 20% 8px 0;display:block;font-size:15px;line-height:1.6;box-shadow:0 2px 8px rgba(0,0,0,0.08);border-left:4px solid #667eea; }
.sys-bubble { background:#fff3cd;color:#856404;padding:10px 16px;border-radius:10px;margin:6px 10%;display:block;font-size:14px;text-align:center; }
.streak-card { background:linear-gradient(135deg,#f093fb,#f5576c);color:white;padding:16px;border-radius:12px;text-align:center;margin:8px 0; }
.streak-num { font-size:42px;font-weight:bold;line-height:1; }
.metric-box { background:white;border-radius:12px;padding:16px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.metric-val { font-size:32px;font-weight:bold;color:#667eea; }
.metric-lbl { font-size:13px;color:#718096;margin-top:4px; }
.stButton > button { border-radius:20px!important;background:linear-gradient(135deg,#667eea,#764ba2)!important;color:white!important;border:none!important;font-weight:600!important; }
.practice-card { background:white;border-radius:12px;padding:14px 18px;margin:8px 0;border-left:5px solid;box-shadow:0 2px 6px rgba(0,0,0,0.06); }
.easy-card{border-color:#48bb78;} .medium-card{border-color:#ed8936;} .hard-card{border-color:#e53e3e;}
.tag{display:inline-block;padding:2px 10px;border-radius:8px;font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px;}
.easy-t{background:#c6f6d5;color:#276749;} .medium-t{background:#feebc8;color:#7b341e;} .hard-t{background:#fed7d7;color:#822727;}
.cbadge{background:#ebf8ff;color:#2b6cb0;border:1px solid #bee3f8;border-radius:12px;padding:3px 10px;font-size:12px;font-weight:600;display:inline-block;margin:2px;}
.sbadge{background:#f0fff4;color:#276749;border:1px solid #c6f6d5;border-radius:12px;padding:3px 10px;font-size:12px;font-weight:600;display:inline-block;margin:2px;}
.abadge{background:#fffaf0;color:#c05621;border:1px solid #fbd38d;border-radius:12px;padding:3px 10px;font-size:12px;font-weight:600;display:inline-block;margin:2px;}
.cmap-center{background:linear-gradient(135deg,#667eea,#764ba2);color:white;border-radius:50px;padding:10px 24px;display:inline-block;font-weight:bold;font-size:16px;}
.cmap-node{background:white;border:2px solid #667eea;border-radius:8px;padding:8px 14px;margin:6px 0;font-size:14px;}
</style>
""", unsafe_allow_html=True)

def init_state():
    for k, v in {
        "messages": [], "session_id": str(uuid.uuid4()),
        "streak": {"streak_days":0,"questions_today":0,"total_questions":0},
        "mode": "student", "generate_audio": False,
        "show_mistake": False, "show_practice": False, "show_cmap": False,
    }.items():
        if k not in st.session_state: st.session_state[k] = v

init_state()

def api_post(ep, payload):
    try:
        r = requests.post(f"{API_URL}{ep}", json=payload, timeout=120)
        r.raise_for_status(); return r.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend offline! Run: uvicorn backend.api.main:app --reload"); return None
    except Exception as e:
        st.error(f"API Error: {e}"); return None

def api_get(ep):
    try:
        r = requests.get(f"{API_URL}{ep}", timeout=30)
        r.raise_for_status(); return r.json()
    except requests.exceptions.ConnectionError:
        st.error("Backend offline!"); return None
    except Exception as e:
        st.error(f"API Error: {e}"); return None

def render_practice(data):
    if not data: return
    qs = data.get("questions", [])
    if not qs: return
    st.markdown("---\n**🎯 Practice Questions:**")
    for q in qs:
        lvl = q.get("level","easy").lower()
        icon = "🟢" if lvl=="easy" else "🟡" if lvl=="medium" else "🔴"
        with st.expander(f"{icon} {lvl.upper()} — {q.get('question','')[:70]}..."):
            st.markdown(f"""<div class='practice-card {lvl}-card'>
                <span class='tag {lvl}-t'>{lvl}</span>
                <p style='font-size:15px;margin:8px 0 12px;'><b>Q:</b> {q.get('question','')}</p>
                <p style='color:#718096;font-size:13px;'>💡 {q.get('hint','')}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("Show Answer 👁️", key=f"ans_{lvl}_{abs(hash(q.get('question','')))}"):
                st.success(f"✅ {q.get('answer','')}")

def render_cmap(data):
    if not data: return
    central = data.get("central_concept","Topic")
    conns   = data.get("connections",[])
    st.markdown("---\n**🗺️ Concept Map:**")
    st.markdown(f"<div style='text-align:center;margin:8px 0'><span class='cmap-center'>🎯 {central}</span></div>",
                unsafe_allow_html=True)
    for c in conns:
        st.markdown(f"""<div style='display:flex;align-items:flex-start;margin:6px 0;'>
            <span style='color:#667eea;font-size:22px;margin:4px 8px 0 8px;'>↕</span>
            <div class='cmap-node'><b>{c.get('related_concept','')}</b>
            <span style='color:#718096;font-size:12px;margin-left:8px;'>({c.get('relationship','')})</span>
            <br><span style='font-size:13px;color:#4a5568;'>{c.get('description','')}</span></div>
        </div>""", unsafe_allow_html=True)

def render_msg(msg):
    role, content = msg["role"], msg["content"]
    if role == "user":
        st.markdown(f"<div class='user-bubble'>👤 {content}</div>", unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f"<div class='sys-bubble'>{content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-bubble'>🤖 {content}</div>", unsafe_allow_html=True)
        meta = msg.get("meta",{})
        b = ""
        if meta.get("topic") and meta["topic"] not in ("general",""):
            b += f"<span class='cbadge'>📌 {meta['topic']}</span>"
        if meta.get("subject") and meta["subject"] not in ("general",""):
            b += f"<span class='sbadge'>📖 {meta['subject']}</span>"
        if meta.get("adaptive_mode"):
            b += "<span class='abadge'>🔄 Simpler mode ON</span>"
        if b: st.markdown(b, unsafe_allow_html=True)
        if msg.get("audio_url"):
            try:
                ar = requests.get(f"{API_URL}{msg['audio_url']}", timeout=10)
                if ar.status_code == 200: st.audio(ar.content, format="audio/wav")
            except Exception: pass
        if msg.get("practice"): render_practice(msg["practice"])
        if msg.get("cmap"):     render_cmap(msg["cmap"])

with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 20px;'>
        <div style='font-size:48px;'>📚</div>
        <div style='font-size:20px;font-weight:bold;color:#667eea;'>NCERT Study Buddy</div>
        <div style='font-size:12px;color:#718096;'>Class 9–10 Science & Maths</div>
    </div>""", unsafe_allow_html=True)
    mode = st.radio("Mode", ["🎓 Student Mode","👩‍🏫 Teacher Dashboard"], label_visibility="collapsed")
    st.session_state.mode = "student" if "Student" in mode else "teacher"
    st.divider()
    if st.session_state.mode == "student":
        s = st.session_state.streak
        sd, qt = s.get("streak_days",0), s.get("questions_today",0)
        st.markdown(f"""<div class='streak-card'>
            <div class='streak-num'>{'🔥' if sd>0 else '💤'} {sd}</div>
            <div style='font-size:13px;opacity:.9;margin-top:4px;'>Day Streak</div>
        </div>""", unsafe_allow_html=True)
        st.progress(min(qt/3,1.0), text=f"Today: {qt}/3 questions")
        if qt < 3: st.info(f"Ask {3-qt} more to earn streak! 💪")
        else:       st.success("Streak earned today! 🎉")
        st.divider()
        st.markdown("**⚡ Quick Actions**")
        if st.button("🎯 Practice Questions", use_container_width=True): st.session_state.show_practice=True
        if st.button("🗺️ Concept Map",        use_container_width=True): st.session_state.show_cmap=True
        if st.button("🔍 Mistake Analyzer",   use_container_width=True): st.session_state.show_mistake=True
        st.divider()
        st.markdown("**🎧 Voice Explanation**")
        st.session_state.generate_audio = st.toggle("Enable voice reply", value=False)
        st.divider()
        if st.button("Check API Status", use_container_width=True):
            h = api_get("/health")
            if h:
                st.success("✅ API Online")
                st.write(f"{'✅' if h.get('ollama_running') else '❌'} Ollama")
                st.write(f"📄 RAG Docs: {h.get('rag_documents',0)}")
        st.divider()
        st.markdown(f"**Session:** `{st.session_state.session_id[:8]}...`")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []; st.rerun()

if st.session_state.mode == "student":
    st.markdown("""<div style='text-align:center;padding:10px 0 16px;'>
        <h1 style='color:#667eea;margin:0;'>📚 NCERT Study Buddy</h1>
        <p style='color:#718096;margin:4px 0 0;'>Hinglish / Tanglish mein pooch — Main samjhaunga! 🤓</p>
    </div>""", unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("**🌟 Try asking:**")
        examples = ["bhai photosynthesis kya hai?","da, Newton law enna sollu",
                    "Quadratic equation kaise karein?","atom vs molecule difference?",
                    "DNA replication epdi nadakkuthu?","sin cos tan trick batao"]
        cols = st.columns(3)
        for i, ex in enumerate(examples):
            with cols[i % 3]:
                if st.button(ex, use_container_width=True, key=f"ex{i}"):
                    st.session_state["_pq"] = ex
        st.divider()

    for msg in st.session_state.messages:
        render_msg(msg)

    if st.session_state.show_mistake:
        st.divider()
        st.markdown("### 🔍 Mistake Analyzer")
        with st.form("mform"):
            c1,c2 = st.columns(2)
            with c1:
                mt = st.text_input("Topic", placeholder="e.g. Newton's Laws")
                mq = st.text_area("Question", height=90)
            with c2:
                ma = st.text_area("Your Wrong Answer", height=120)
            cs, cc = st.columns(2)
            with cs: sub_m = st.form_submit_button("🔍 Analyze", use_container_width=True)
            with cc: can_m = st.form_submit_button("Cancel", use_container_width=True)
        if can_m: st.session_state.show_mistake=False; st.rerun()
        if sub_m and mt and mq and ma:
            with st.spinner("Analyzing..."):
                res = api_post("/analyze-mistake",{"session_id":st.session_state.session_id,"topic":mt,"question":mq,"student_answer":ma})
            if res:
                st.session_state.messages += [
                    {"role":"system","content":f"🔍 Mistake Analysis — {mt}"},
                    {"role":"assistant","content":res.get("analysis",""),"meta":{"topic":mt}}]
                st.session_state.show_mistake=False; st.rerun()

    if st.session_state.show_practice:
        st.divider()
        st.markdown("### 🎯 Practice Question Generator")
        with st.form("pform"):
            c1,c2 = st.columns(2)
            with c1: pt = st.text_input("Topic", placeholder="e.g. Photosynthesis, Motion")
            with c2: ps = st.selectbox("Subject",["general","science_biology","science_physics","science_chemistry","mathematics"])
            gen_p = st.form_submit_button("⚡ Generate 3 Questions", use_container_width=True)
        if gen_p and pt:
            with st.spinner("Generating questions..."):
                res = api_post("/practice",{"session_id":st.session_state.session_id,"topic":pt,"subject":ps})
            if res and res.get("practice_questions"):
                st.session_state.messages += [
                    {"role":"system","content":f"🎯 Practice: **{pt}**"},
                    {"role":"assistant","content":f"Yeh lo tere liye {pt} pe 3 questions — Easy se Hard tak! 💪",
                     "meta":{"topic":pt},"practice":res["practice_questions"]}]
                st.session_state.show_practice=False; st.rerun()

    if st.session_state.show_cmap:
        st.divider()
        st.markdown("### 🗺️ Concept Map")
        with st.form("cmform"):
            c1,c2 = st.columns(2)
            with c1: cmt = st.text_input("Topic", placeholder="e.g. Photosynthesis")
            with c2: cms = st.selectbox("Subject",["general","science_biology","science_physics","science_chemistry","mathematics"])
            gen_cm = st.form_submit_button("🗺️ Generate Map", use_container_width=True)
        if gen_cm and cmt:
            with st.spinner("Building concept map..."):
                res = api_get(f"/concept-map/{cmt}?subject={cms}")
            if res:
                st.session_state.messages += [
                    {"role":"system","content":f"🗺️ Concept Map: **{cmt}**"},
                    {"role":"assistant","content":f"Yeh dekh — {cmt} kaise connect hota hai! 🌐",
                     "meta":{"topic":cmt},"cmap":res}]
                st.session_state.show_cmap=False; st.rerun()

    st.divider()
    default_q = st.session_state.pop("_pq","")
    ci, cb = st.columns([5,1])
    with ci:
        user_input = st.text_input("Ask your doubt...",value=default_q,
            placeholder="bhai photosynthesis kya hai? / da, force enna?",
            label_visibility="collapsed",key="cinput")
    with cb:
        send = st.button("Send 📨", use_container_width=True)

    if (send or default_q) and user_input.strip():
        q = user_input.strip()
        st.session_state.messages.append({"role":"user","content":q})
        with st.spinner("Soch raha hoon..."):
            res = api_post("/chat",{"question":q,"session_id":st.session_state.session_id,
                           "generate_audio":st.session_state.generate_audio})
        if res:
            st.session_state.messages.append({
                "role":"assistant","content":res.get("response","Kuch problem, dobara try karo!"),
                "meta":{"topic":res.get("topic",""),"subject":res.get("subject",""),
                        "adaptive_mode":res.get("adaptive_mode",False)},
                "audio_url":res.get("audio_url")})
            if res.get("streak"): st.session_state.streak = res["streak"]
        st.rerun()

else:
    st.markdown("""<div style='text-align:center;padding:10px 0 20px;'>
        <h1 style='color:#667eea;margin:0;'>👩‍🏫 Teacher Analytics Dashboard</h1>
        <p style='color:#718096;margin:4px 0 0;'>Class-wide insights — no individual student data exposed</p>
    </div>""", unsafe_allow_html=True)

    with st.spinner("Loading analytics..."):
        data = api_get("/teacher/dashboard")
    if not data: st.warning("Could not load data."); st.stop()

    ints = data.get("interactions",{})
    m1,m2,m3,m4 = st.columns(4)
    for col, val, lbl in zip([m1,m2,m3,m4],
        [ints.get("total_interactions",0),ints.get("this_week",0),ints.get("today",0),ints.get("unique_students",0)],
        ["Total Questions","This Week","Today","Unique Students"]):
        with col: st.markdown(f"<div class='metric-box'><div class='metric-val'>{val}</div><div class='metric-lbl'>{lbl}</div></div>",
                              unsafe_allow_html=True)

    st.divider()
    l, r = st.columns(2)
    with l:
        st.markdown("### 🔥 Most Asked Topics (Last 7 Days)")
        tops = data.get("top_topics",[])
        if tops:
            import pandas as pd
            df = pd.DataFrame(tops); df.columns=["Topic","Subject","Times Asked"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else: st.info("No topic data yet.")
    with r:
        st.markdown("### 📊 Subject Distribution")
        sd = data.get("subject_distribution",[])
        if sd:
            st.bar_chart({row["subject"]:row["count"] for row in sd})
        else: st.info("No data yet.")

    st.divider()
    st.markdown("### 🎯 Concept Difficulty Trends")
    trends = data.get("difficulty_trends",[])
    if trends:
        for t in trends[:10]:
            lvl = t.get("difficulty_level","Low")
            color = "#e53e3e" if lvl=="High" else "#ed8936" if lvl=="Medium" else "#48bb78"
            ct,cpb,cd = st.columns([3,2,1])
            with ct: st.write(f"**{t['topic']}** ({t.get('total_asks',0)} asks)")
            with cpb: st.progress(min(t.get("repeat_rate",0)/100,1.0),text=f"Repeat: {t.get('repeat_rate',0)}%")
            with cd: st.markdown(f"<span style='color:{color};font-weight:bold;'>{lvl}</span>",unsafe_allow_html=True)
    else: st.info("Not enough data yet.")

    st.divider()
    st.markdown("### 📅 Daily Activity (Last 7 Days)")
    daily = data.get("daily_activity",[])
    if daily:
        import pandas as pd
        df_d = pd.DataFrame(daily).set_index("date")
        st.line_chart(df_d["questions"])
    else: st.info("No daily data yet.")
