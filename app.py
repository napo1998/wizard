# Created by Napoleon Perez
import streamlit as st
import json
import math
import base64
import os
from datetime import datetime

def _img_b64(filename: str) -> str:
    """Return a base64 data-URI for an image file located next to app.py."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, filename)
    ext  = filename.rsplit(".", 1)[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Prompt Optimization Wizard",
    page_icon="✨",
    layout="wide",
)

# ── Global CSS theme ──────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base & Background ───────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: #f0f6ff;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
[data-testid="stMain"] { background: transparent; }

/* ── Global text ─────────────────────────────────────────────── */
body, p, span, div, label, li, td, th,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #111827;
}

/* ── Headings ────────────────────────────────────────────────── */
h1, h2, h3, h4 {
    color: #1e3a5f !important;
    -webkit-text-fill-color: #1e3a5f !important;
    font-weight: 800 !important;
    letter-spacing: -0.3px !important;
}

/* ── Caption / helper text ───────────────────────────────────── */
[data-testid="stCaptionContainer"] p, small {
    color: #4b5563 !important;
    font-size: 0.875rem !important;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1f44 0%, #1a3a8f 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #dbeafe !important;
    -webkit-text-fill-color: #dbeafe !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.20) !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.20) !important;
    border-color: rgba(255,255,255,0.35) !important;
}

/* ── Primary buttons ─────────────────────────────────────────── */
button[kind="primary"] {
    background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.40) !important;
    transition: all 0.2s ease !important;
}
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Secondary buttons ───────────────────────────────────────── */
button[kind="secondary"] {
    border-radius: 12px !important;
    border: 2px solid #bfdbfe !important;
    color: #1d4ed8 !important;
    -webkit-text-fill-color: #1d4ed8 !important;
    background: #ffffff !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
button[kind="secondary"]:hover {
    background: #eff6ff !important;
    border-color: #2563eb !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.15) !important;
}

/* ── Progress bar ────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div {
    background-color: #dbeafe !important;
    border-radius: 99px !important;
    height: 8px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #2563eb, #38bdf8) !important;
    border-radius: 99px !important;
}

/* ── Textarea ────────────────────────────────────────────────── */
textarea {
    border-radius: 12px !important;
    border: 2px solid #bfdbfe !important;
    color: #111827 !important;
    background-color: #ffffff !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,0.12) !important;
    background-color: #ffffff !important;
}

/* ── Info / success / warning boxes ─────────────────────────── */
[data-testid="stInfo"] {
    background: #eff6ff !important;
    border-left: 4px solid #3b82f6 !important;
    border-radius: 10px !important;
    color: #1e3a5f !important;
}
[data-testid="stSuccess"] {
    background: #f0fdf4 !important;
    border-left: 4px solid #22c55e !important;
    border-radius: 10px !important;
}
[data-testid="stWarning"] {
    background: #fffbeb !important;
    border-left: 4px solid #f59e0b !important;
    border-radius: 10px !important;
}

/* ── Code block ──────────────────────────────────────────────── */
[data-testid="stCode"] {
    border-radius: 12px !important;
    border: 1px solid #bfdbfe !important;
}

/* ── Divider ─────────────────────────────────────────────────── */
hr { border-color: #dbeafe !important; }

/* ── File uploader ───────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed #93c5fd !important;
    border-radius: 12px !important;
    background: #f8fbff !important;
}

/* ── Expander ────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #dbeafe !important;
    border-radius: 12px !important;
    background: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
LLM_OPTIONS = [
    {"id": "claude",  "name": "Claude",      "color": "🟠",
     "desc": "Anthropic's Claude models",
     "strengths": ["XML tags", "Thinking tags", "Detailed reasoning", "Role clarity"],
     "context_limit": 200_000, "cost_per_1k": 0.008},
    {"id": "gpt4",    "name": "GPT-4",       "color": "🟢",
     "desc": "OpenAI's GPT-4 models",
     "strengths": ["System messages", "Step-by-step", "Few-shot examples", "JSON output"],
     "context_limit": 128_000, "cost_per_1k": 0.03},
    {"id": "gemini",  "name": "Gemini",      "color": "🔵",
     "desc": "Google's Gemini models",
     "strengths": ["Multimodal", "Conversational", "Long context", "Structured data"],
     "context_limit": 1_000_000, "cost_per_1k": 0.0015},
    {"id": "llama",   "name": "Llama",       "color": "🟣",
     "desc": "Meta's Llama models",
     "strengths": ["Instruction following", "Code generation", "Reasoning", "Open source"],
     "context_limit": 8_192, "cost_per_1k": 0.0002},
    {"id": "other",   "name": "Other/Local", "color": "⚫",
     "desc": "Other or local models",
     "strengths": ["Privacy", "Customization", "Local processing", "Cost effective"],
     "context_limit": 4_096, "cost_per_1k": 0.0},
]

LLM_TIPS = {
    "claude":  ["Use XML tags like <role>, <task>, <context>",
                "Add <thinking> for complex reasoning",
                "Be explicit about desired output format",
                "Works great with step-by-step instructions"],
    "gpt4":   ["Use system messages for behaviour & constraints",
               "Provide few-shot examples for consistency",
               "Use 'Let's think step by step' for complex tasks",
               "Specify JSON schema for structured output"],
    "gemini": ["Leverage multimodal capabilities when relevant",
               "Use conversational, natural language",
               "Take advantage of the huge context window",
               "Structure data clearly for better processing"],
    "llama":  ["Use clear, direct instructions",
               "Provide context before the main task",
               "Keep consistent formatting throughout",
               "Keep prompts concise but complete"],
    "other":  ["Test prompt length limits for your model",
               "Use simple, clear language",
               "Provide explicit examples",
               "Keep formatting minimal and consistent"],
}

EXPERIENCE_LEVELS = [
    {"id": "beginner",     "title": "Beginner",
     "desc": "New to AI prompting — I want detailed guidance and explanations",
     "features": ["Step-by-step explanations", "Detailed tips and examples", "Best-practice guidance"]},
    {"id": "intermediate", "title": "Intermediate",
     "desc": "Some experience — I know the basics but want optimisation help",
     "features": ["Streamlined questions", "Advanced techniques", "Optional deep-dives"]},
    {"id": "advanced",     "title": "Advanced",
     "desc": "Experienced prompter — I want efficient tools and advanced features",
     "features": ["Quick setup", "Advanced optimisation", "Custom techniques"]},
]

QUESTIONS = {
    "beginner": [
        {"key": "task",    "q": "What do you want the AI to do?",
         "hint": "Be specific! E.g. 'write a professional email to decline a meeting'",
         "ph": "e.g. Write a product description for an eco-friendly water bottle…"},
        {"key": "context", "q": "What background information should the AI know?",
         "hint": "Include relevant details, constraints, and important context",
         "ph": "e.g. Targeting sustainability-minded millennials…"},
        {"key": "role",    "q": "What role should the AI take on?",
         "hint": "Giving the AI a role helps it understand the perspective",
         "ph": "e.g. Act as an experienced marketing copywriter…"},
        {"key": "format",  "q": "How should the output be formatted?",
         "hint": "Specify structure, length, style, or format requirements",
         "ph": "e.g. Provide 3 different versions, each under 100 words…"},
        {"key": "tone",    "q": "What tone or style should it use?",
         "hint": "Consider your audience and purpose",
         "ph": "e.g. Professional but approachable, enthusiastic about sustainability…"},
    ],
    "intermediate": [
        {"key": "task",    "q": "Primary task and objective",
         "hint": "Define the main goal and any sub-objectives",
         "ph": "Task definition and expected outcomes…"},
        {"key": "context", "q": "Context and constraints",
         "hint": "Include background, limitations, and success criteria",
         "ph": "Relevant background information and constraints…"},
        {"key": "role",    "q": "Role and expertise level",
         "hint": "Define the persona and domain expertise needed",
         "ph": "Expert role and relevant experience…"},
        {"key": "format",  "q": "Output format and structure",
         "hint": "Specify format, length, and structural requirements",
         "ph": "Desired format and organisation…"},
    ],
    "advanced": [
        {"key": "task",    "q": "Task specification",
         "hint": "Precise task definition with success metrics",
         "ph": "Detailed task specification…"},
        {"key": "context", "q": "Context and parameters",
         "hint": "All relevant context, constraints, and parameters",
         "ph": "Comprehensive context…"},
        {"key": "format",  "q": "Output requirements",
         "hint": "Exact format, structure, and validation criteria",
         "ph": "Specific output format and requirements…"},
    ],
}

# ── Helper functions ───────────────────────────────────────────────────────────

def llm_by_id(llm_id):
    return next((l for l in LLM_OPTIONS if l["id"] == llm_id), LLM_OPTIONS[-1])

def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / 4)

def generate_prompt(llm_id: str, data: dict) -> str:
    task    = data.get("task", "")
    context = data.get("context", "")
    role    = data.get("role", "You are a helpful AI assistant.")
    fmt     = data.get("format", "")
    tone    = data.get("tone", "")
    constr  = data.get("constraints", "")

    if llm_id == "claude":
        parts = [
            f"<role>\n{role}\n</role>",
            f"<task>\n{task}\n</task>",
            f"<context>\n{context}\n</context>",
        ]
        if fmt:    parts.append(f"<format>\n{fmt}\n</format>")
        if tone:   parts.append(f"<tone>{tone}</tone>")
        if constr: parts.append(f"<constraints>{constr}</constraints>")
        parts.append("Please complete this task following the specifications above.")
        return "\n\n".join(parts)

    if llm_id == "gpt4":
        sys = f"System: {role}"
        if constr: sys += f" {constr}"
        lines = [sys, f"\nTask: {task}", f"Context: {context}"]
        if fmt:  lines.append(f"Format Requirements: {fmt}")
        if tone: lines.append(f"Tone: {tone}")
        lines.append("\nPlease complete this task according to the specifications above.")
        return "\n".join(lines)

    # gemini / llama / other
    lines = [f"{role}\n" if role else ""]
    lines.append(f"Task: {task}")
    lines.append(f"Context: {context}")
    if fmt:    lines.append(f"Format: {fmt}")
    if tone:   lines.append(f"Tone: {tone}")
    if constr: lines.append(f"Constraints: {constr}")
    lines.append("\nPlease complete this task according to the specifications above.")
    return "\n".join(l for l in lines if l)

def get_suggestions(data: dict) -> list[str]:
    s = []
    if not data.get("role"):    s.append("Consider adding a specific role for the AI")
    if not data.get("context"): s.append("Add more context for better results")
    if not data.get("format"):  s.append("Specify your desired output format")
    if len(data.get("task", "")) < 20:
        s.append("Your task description could be more detailed")
    return s

def optimization_score(suggestions: list) -> int:
    return max(50, 100 - len(suggestions) * 15)

def get_warnings(prompt: str, llm_id: str) -> list[dict]:
    w = []
    llm = llm_by_id(llm_id)
    tokens = estimate_tokens(prompt)
    pct = tokens / llm["context_limit"] * 100
    if pct > 90:
        w.append({"type": "error",
                  "msg": f"Very close to {llm['name']}'s limit ({tokens:,}/{llm['context_limit']:,} tokens)"})
    elif pct > 70:
        w.append({"type": "warning",
                  "msg": f"Getting long for {llm['name']} ({tokens:,}/{llm['context_limit']:,} tokens)"})
    if llm_id != "claude" and "<" in prompt and ">" in prompt:
        w.append({"type": "warning",
                  "msg": "XML tags work best with Claude. Consider plain text for this model."})
    if llm_id == "llama" and tokens > 2000:
        w.append({"type": "warning",
                  "msg": "Llama models work better with shorter, more concise prompts."})
    return w

# ── Session state init ─────────────────────────────────────────────────────────

DEFAULTS = dict(
    step="welcome",         # welcome | llm | experience | mode | guided | editor | result
    selected_llm="",
    experience="",
    mode="",
    q_index=0,
    prompt_data=dict(task="", context="", role="", format="", tone="", constraints=""),
    current_prompt="",
    history=[],
)

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🔄 Start Over", use_container_width=True):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v if k != "history" else st.session_state.history
        st.rerun()

    st.divider()
    st.subheader("💾 Export / Import")

    if st.session_state.current_prompt:
        export_obj = dict(
            version="1.0",
            timestamp=datetime.now().isoformat(),
            llm=st.session_state.selected_llm,
            experience=st.session_state.experience,
            mode=st.session_state.mode,
            prompt_data=st.session_state.prompt_data,
            current_prompt=st.session_state.current_prompt,
        )
        st.download_button(
            "⬇️ Export prompt (.json)",
            data=json.dumps(export_obj, indent=2),
            file_name=f"prompt-{datetime.now().strftime('%Y-%m-%d')}.json",
            mime="application/json",
            use_container_width=True,
        )

    uploaded = st.file_uploader("⬆️ Import prompt (.json)", type="json")
    if uploaded:
        try:
            imp = json.loads(uploaded.read())
            st.session_state.selected_llm   = imp.get("llm", "")
            st.session_state.experience     = imp.get("experience", "intermediate")
            st.session_state.mode           = imp.get("mode", "guided")
            st.session_state.prompt_data    = imp.get("prompt_data", DEFAULTS["prompt_data"])
            st.session_state.current_prompt = imp.get("current_prompt", "")
            st.session_state.step           = "result"
            st.success("Imported!")
            st.rerun()
        except Exception:
            st.error("Invalid file format.")

    st.divider()
    st.subheader(f"📚 History ({len(st.session_state.history)})")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            llm_name = llm_by_id(item["llm"])["name"]
            with st.expander(f"#{len(st.session_state.history)-i} · {llm_name} · {item['title'][:30]}"):
                st.caption(item["timestamp"])
                st.text_area("Preview", item["current_prompt"][:300] + "…",
                             height=100, disabled=True, key=f"hist_prev_{i}")
                if st.button("Restore", key=f"hist_restore_{i}"):
                    st.session_state.selected_llm   = item["llm"]
                    st.session_state.experience     = item.get("experience", "intermediate")
                    st.session_state.mode           = item.get("mode", "guided")
                    st.session_state.prompt_data    = item["prompt_data"]
                    st.session_state.current_prompt = item["current_prompt"]
                    st.session_state.step           = "result"
                    st.rerun()
    else:
        st.caption("No saved prompts yet.")

# ── Step router ────────────────────────────────────────────────────────────────

step = st.session_state.step

# ─────────────────────────────────────────────────────────────────────────────
# STEP: WELCOME
# ─────────────────────────────────────────────────────────────────────────────
if step == "welcome":
    # ── Hero banner ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 100%);
        border-radius: 22px;
        padding: 64px 52px 56px 52px;
        margin-bottom: 36px;
        box-shadow: 0 12px 48px rgba(29,78,216,0.22);
    ">
        <div style="font-size:3.6rem;font-weight:900;color:white;letter-spacing:-1px;line-height:1.1;">
            ✨ LLM Prompt Optimization Wizard
        </div>
        <div style="font-size:1.45rem;color:#bfdbfe;margin-top:16px;font-weight:400;">
            Create perfectly optimised prompts tailored to your LLM
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Author + AI badge row ──────────────────────────────────────────────
    _a_col, _b_col, _spacer = st.columns([2, 2, 6])
    with _a_col:
        try:
            napo_src = _img_b64("napo.jpg")
        except Exception:
            napo_src = ""
        napo_img_tag = f"<img src='{napo_src}' width='90' style='border-radius:50%;border:3px solid #2563eb;'>" if napo_src else ""
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;
            background:white;border-radius:16px;padding:16px 20px;
            border:1px solid #bfdbfe;box-shadow:0 4px 16px rgba(37,99,235,0.10);">
            {napo_img_tag}
            <div>
                <div style="font-size:13px;color:#6b7280;">Created by</div>
                <a href="https://www.linkedin.com/in/napo1998/" target="_blank"
                   style="font-weight:800;color:#1d4ed8;text-decoration:none;font-size:16px;">
                   Napoleon Perez
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with _b_col:
        try:
            ai_src = _img_b64("image.png")
        except Exception:
            ai_src = ""
        ai_img_tag = f"<img src='{ai_src}' width='56' style='border-radius:10px;'>" if ai_src else ""
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;
            background:white;border-radius:16px;padding:16px 20px;
            border:1px solid #bfdbfe;box-shadow:0 4px 16px rgba(37,99,235,0.10);">
            {ai_img_tag}
            <div>
                <div style="font-size:13px;color:#6b7280;">Empowered by</div>
                <div style="font-weight:800;color:#1d4ed8;font-size:16px;">AI Community</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature cards ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:white;border-radius:14px;padding:22px;
            border:1px solid #bfdbfe;box-shadow:0 2px 12px rgba(37,99,235,0.07);
            text-align:center;">
            <div style="font-size:2rem;">🧠</div>
            <div style="font-weight:700;color:#1d4ed8;margin:8px 0 6px;">LLM-Specific Optimization</div>
            <div style="font-size:13px;color:#6b7280;">Tailored advice for Claude, GPT-4, Gemini, and more</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:white;border-radius:14px;padding:22px;
            border:1px solid #bfdbfe;box-shadow:0 2px 12px rgba(37,99,235,0.07);
            text-align:center;">
            <div style="font-size:2rem;">💬</div>
            <div style="font-weight:700;color:#1d4ed8;margin:8px 0 6px;">Smart Validation & History</div>
            <div style="font-size:13px;color:#6b7280;">Token counting, warnings, and prompt history</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:white;border-radius:14px;padding:22px;
            border:1px solid #bfdbfe;box-shadow:0 2px 12px rgba(37,99,235,0.07);
            text-align:center;">
            <div style="font-size:2rem;">✏️</div>
            <div style="font-weight:700;color:#1d4ed8;margin:8px 0 6px;">Import & Export</div>
            <div style="font-size:13px;color:#6b7280;">Save and share your optimised prompts</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Building Your Perfect Prompt", type="primary", use_container_width=True):
        st.session_state.step = "llm"
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: LLM SELECTION
# ─────────────────────────────────────────────────────────────────────────────
elif step == "llm":
    st.markdown("## 1 · Choose Your LLM")
    st.caption("Different models work best with different prompting approaches")

    cols = st.columns(len(LLM_OPTIONS))
    for col, llm in zip(cols, LLM_OPTIONS):
        with col:
            selected = st.session_state.selected_llm == llm["id"]
            border = "2px solid #2563eb" if selected else "1px solid #dbeafe"
            bg     = "#eff6ff" if selected else "#ffffff"
            shadow = "0 4px 20px rgba(37,99,235,0.18)" if selected else "0 2px 8px rgba(37,99,235,0.07)"
            cost_html = f"<div style='color:#111827;font-size:12px;'>💰 ${llm['cost_per_1k']}/1k tokens</div>" if llm['cost_per_1k'] else ""
            strengths_html = "<br>".join(f"• {s}" for s in llm['strengths'][:3])
            st.markdown(
                f"""<div style="border:{border};border-radius:14px;padding:18px 14px;
                    background:{bg};min-height:220px;box-shadow:{shadow};
                    transition:all 0.2s;">
                    <div style="font-size:1.1rem;font-weight:700;color:#111827;margin-bottom:4px;">
                        {llm['color']} {llm['name']}
                    </div>
                    <div style="color:#374151;font-size:12px;margin-bottom:10px;">{llm['desc']}</div>
                    <div style="color:#111827;font-size:12px;">📏 {llm['context_limit']:,} tokens</div>
                    {cost_html}
                    <div style="margin-top:10px;color:#111827;font-size:12px;">
                        <b>Strengths:</b><br>{strengths_html}
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"Select {llm['name']}", key=f"llm_{llm['id']}",
                         type="primary" if selected else "secondary",
                         use_container_width=True):
                st.session_state.selected_llm = llm["id"]
                st.rerun()

    if st.session_state.selected_llm:
        llm = llm_by_id(st.session_state.selected_llm)
        st.markdown(f"### 💡 Tips for {llm['name']}")
        tip_cols = st.columns(2)
        for i, tip in enumerate(LLM_TIPS.get(st.session_state.selected_llm, [])):
            tip_cols[i % 2].success(f"✓ {tip}")

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = "welcome"; st.rerun()
    with c2:
        if st.button("Continue →", type="primary", use_container_width=True,
                     disabled=not st.session_state.selected_llm):
            st.session_state.step = "experience"; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: EXPERIENCE LEVEL
# ─────────────────────────────────────────────────────────────────────────────
elif step == "experience":
    st.markdown("## 2 · What's Your Experience Level?")
    st.caption("We'll adapt the interface and guidance to match your expertise")

    for level in EXPERIENCE_LEVELS:
        selected = st.session_state.experience == level["id"]
        bg        = "#eff6ff" if selected else "#ffffff"
        border    = "2px solid #2563eb" if selected else "1px solid #dbeafe"
        shadow    = "0 4px 20px rgba(37,99,235,0.15)" if selected else "0 2px 8px rgba(37,99,235,0.06)"
        title_col = "#1d4ed8" if selected else "#1e3a5f"
        badge_bg  = "#2563eb" if selected else "#dbeafe"
        badge_col = "#ffffff" if selected else "#1d4ed8"
        check     = "✅ " if selected else ""
        badges    = "".join(
            f"<span style='background:{badge_bg};color:{badge_col};border-radius:20px;"
            f"padding:3px 12px;margin-right:6px;font-size:12px;font-weight:600;'>{f}</span>"
            for f in level["features"]
        )
        st.markdown(
            f"""<div style="border:{border};border-radius:16px;padding:24px 28px;
                background:{bg};margin-bottom:4px;box-shadow:{shadow};">
                <div style="font-size:1.15rem;font-weight:800;color:{title_col};margin-bottom:6px;">
                    {check}{level['title']}
                </div>
                <div style="color:#374151;font-size:14px;margin-bottom:14px;">{level['desc']}</div>
                <div>{badges}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button(f"Choose {level['title']}", key=f"exp_{level['id']}",
                     type="primary" if selected else "secondary",
                     use_container_width=True):
            st.session_state.experience = level["id"]; st.rerun()

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = "llm"; st.rerun()
    with c2:
        if st.button("Continue →", type="primary", use_container_width=True,
                     disabled=not st.session_state.experience):
            st.session_state.step = "mode"; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: MODE
# ─────────────────────────────────────────────────────────────────────────────
elif step == "mode":
    st.markdown("## 3 · Choose Your Mode")
    st.caption("How would you like to build your prompt?")

    mc1, mc2 = st.columns(2)
    with mc1:
        g_selected = st.session_state.mode == "guided"
        g_border = "2px solid #2563eb" if g_selected else "1px solid #e5e7eb"
        st.markdown(
            f"""<div style="border:{g_border};border-radius:12px;padding:24px;background:{'#dbeafe' if g_selected else '#fff'};text-align:center;">
            <h3>💬 Guided Questionnaire</h3>
            <p style="color:#6b7280">Step-by-step questions to build your perfect prompt</p>
            <br>✅ Perfect for beginners<br>✅ Ensures all best practices<br>✅ Contextual help & tips
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Select Guided", type="primary" if g_selected else "secondary",
                     use_container_width=True):
            st.session_state.mode = "guided"; st.rerun()

    with mc2:
        e_selected = st.session_state.mode == "editor"
        e_border = "2px solid #2563eb" if e_selected else "1px solid #e5e7eb"
        st.markdown(
            f"""<div style="border:{e_border};border-radius:12px;padding:24px;background:{'#dbeafe' if e_selected else '#fff'};text-align:center;">
            <h3>✏️ Editor Mode</h3>
            <p style="color:#6b7280">Direct editing with real-time optimisation suggestions</p>
            <br>✅ Real-time feedback<br>✅ Full creative control<br>✅ Live optimisation scoring
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Select Editor", type="primary" if e_selected else "secondary",
                     use_container_width=True):
            st.session_state.mode = "editor"; st.rerun()

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = "experience"; st.rerun()
    with c2:
        if st.button("Start Building →", type="primary", use_container_width=True,
                     disabled=not st.session_state.mode):
            st.session_state.step = st.session_state.mode; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: GUIDED QUESTIONNAIRE
# ─────────────────────────────────────────────────────────────────────────────
elif step == "guided":
    questions = QUESTIONS.get(st.session_state.experience, QUESTIONS["beginner"])
    qi = st.session_state.q_index
    qi = max(0, min(qi, len(questions) - 1))
    q  = questions[qi]

    st.markdown(f"## 4 · Building Your Prompt")
    progress = (qi + 1) / len(questions)
    st.progress(progress, text=f"Question {qi+1} of {len(questions)}")

    st.markdown(f"### {q['q']}")
    st.caption(q["hint"])

    val = st.text_area("Your answer", value=st.session_state.prompt_data.get(q["key"], ""),
                       placeholder=q["ph"], height=160, key=f"qa_{qi}")
    st.session_state.prompt_data[q["key"]] = val

    llm_tips = LLM_TIPS.get(st.session_state.selected_llm, LLM_TIPS["other"])
    st.info(f"💡 **Tip for {llm_by_id(st.session_state.selected_llm)['name']}:** "
            f"{llm_tips[qi % len(llm_tips)]}")

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            if qi > 0:
                st.session_state.q_index = qi - 1
            else:
                st.session_state.step = "mode"
            st.rerun()
    with c2:
        last = (qi == len(questions) - 1)
        label = "Generate Prompt →" if last else "Next →"
        if st.button(label, type="primary", use_container_width=True, disabled=not val.strip()):
            if last:
                st.session_state.current_prompt = generate_prompt(
                    st.session_state.selected_llm, st.session_state.prompt_data)
                st.session_state.step = "result"
            else:
                st.session_state.q_index = qi + 1
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: EDITOR MODE
# ─────────────────────────────────────────────────────────────────────────────
elif step == "editor":
    st.markdown("## 4 · Editor Mode")
    st.caption("Write your prompt and get real-time optimisation feedback")

    llm = llm_by_id(st.session_state.selected_llm)

    ec1, ec2 = st.columns([2, 1])
    with ec1:
        st.markdown("### Your Prompt")
        draft = st.text_area("Prompt", value=st.session_state.current_prompt,
                             placeholder="Start typing your prompt here…",
                             height=380, key="editor_area", label_visibility="collapsed")
        st.session_state.current_prompt = draft

        # Token counter
        tokens = estimate_tokens(draft)
        pct    = tokens / llm["context_limit"]
        colour = "red" if pct > 0.9 else "orange" if pct > 0.7 else "green"
        st.markdown(
            f"<small style='color:{colour}'>🔢 {tokens:,} / {llm['context_limit']:,} tokens "
            f"({pct*100:.1f}%) | {len(draft):,} chars"
            + (f" | 💰 ${tokens/1000*llm['cost_per_1k']:.4f}" if llm["cost_per_1k"] else "")
            + "</small>",
            unsafe_allow_html=True,
        )
        st.progress(min(pct, 1.0))

        # Warnings
        for w in get_warnings(draft, st.session_state.selected_llm):
            if w["type"] == "error": st.error(f"⛔ {w['msg']}")
            else: st.warning(f"⚠️ {w['msg']}")

    with ec2:
        st.markdown(f"### 💡 {llm['name']} Tips")
        for tip in LLM_TIPS.get(st.session_state.selected_llm, []):
            st.success(f"✓ {tip}")

        sugg = get_suggestions(st.session_state.prompt_data)
        if sugg:
            st.markdown("### ⚠️ Suggestions")
            for s in sugg:
                st.warning(s)

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.step = "mode"; st.rerun()
    with c2:
        if st.button("Optimize & Analyze →", type="primary", use_container_width=True,
                     disabled=not draft.strip()):
            st.session_state.step = "result"; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP: RESULT
# ─────────────────────────────────────────────────────────────────────────────
elif step == "result":
    st.markdown("## ✅ Your Optimised Prompt")
    llm = llm_by_id(st.session_state.selected_llm)
    st.caption(f"Ready to use with {llm['color']} **{llm['name']}**")

    sugg  = get_suggestions(st.session_state.prompt_data)
    score = optimization_score(sugg)
    warns = get_warnings(st.session_state.current_prompt, st.session_state.selected_llm)

    for w in warns:
        if w["type"] == "error": st.error(f"⛔ {w['msg']}")
        else: st.warning(f"⚠️ {w['msg']}")

    rc1, rc2 = st.columns([2, 1])

    with rc1:
        st.markdown("### Final Prompt")
        edited = st.text_area("Edit if needed", value=st.session_state.current_prompt,
                              height=380, key="result_area", label_visibility="collapsed")
        st.session_state.current_prompt = edited

        tokens = estimate_tokens(edited)
        pct    = tokens / llm["context_limit"]
        colour = "red" if pct > 0.9 else "orange" if pct > 0.7 else "green"
        st.markdown(
            f"<small style='color:{colour}'>🔢 {tokens:,} / {llm['context_limit']:,} tokens "
            f"({pct*100:.1f}%) | {len(edited):,} chars"
            + (f" | 💰 ${tokens/1000*llm['cost_per_1k']:.4f}" if llm["cost_per_1k"] else "")
            + "</small>",
            unsafe_allow_html=True,
        )
        st.progress(min(pct, 1.0))

        st.code(edited, language="")  # nicely formatted read-only copy

        if st.button("💾 Save to History", use_container_width=True):
            st.session_state.history.append(dict(
                id=int(datetime.now().timestamp()),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
                title=st.session_state.prompt_data.get("task", "Untitled")[:60],
                llm=st.session_state.selected_llm,
                experience=st.session_state.experience,
                mode=st.session_state.mode,
                prompt_data=st.session_state.prompt_data,
                current_prompt=edited,
                tokens=tokens,
            ))
            st.success("Saved to history!")

    with rc2:
        st.markdown("### 📊 Optimization Score")
        clr = "#22c55e" if score >= 85 else "#f59e0b" if score >= 70 else "#ef4444"
        st.markdown(
            f"""<div style="text-align:center;padding:24px;border-radius:12px;
                background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1px solid #bfdbfe;
                box-shadow:0 4px 20px rgba(37,99,235,0.10);">
                <div style="font-size:3rem;font-weight:bold;color:{clr}">{score}%</div>
                <div style="color:#6b7280;margin-top:4px">{'🌟 Excellent!' if score>=85 else '👍 Good' if score>=70 else '⚠️ Needs work'}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.progress(score / 100)

        if sugg:
            st.markdown("### 🔧 Improvements")
            for s in sugg:
                st.warning(f"• {s}")
        else:
            st.success("🎉 All components present!")

        st.markdown(f"### 💡 {llm['name']} Tips")
        for tip in LLM_TIPS.get(st.session_state.selected_llm, []):
            st.info(f"✓ {tip}")

    st.markdown("---")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Edit Prompt", use_container_width=True):
            st.session_state.step = st.session_state.mode; st.rerun()
    with c2:
        if st.button("🔄 Create New Prompt", type="primary", use_container_width=True):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v if k != "history" else st.session_state.history
            st.rerun()
