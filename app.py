import streamlit as st
import json
import math
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Prompt Optimization Wizard",
    page_icon="✨",
    layout="wide",
)

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
    st.markdown("# ✨ LLM Prompt Optimization Wizard")
    st.markdown("### Create perfectly optimised prompts tailored to your LLM")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🧠 **LLM-Specific Optimization**\n\nTailored advice for Claude, GPT-4, Gemini, and more")
    with col2:
        st.success("💬 **Smart Validation & History**\n\nToken counting, warnings, and prompt history")
    with col3:
        st.warning("✏️ **Import & Export**\n\nSave and share your optimised prompts")

    st.markdown("---")
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
            border = "2px solid #6366f1" if selected else "1px solid #e5e7eb"
            bg     = "#eef2ff" if selected else "#ffffff"
            st.markdown(
                f"""<div style="border:{border};border-radius:12px;padding:16px;background:{bg};min-height:200px;">
                <b>{llm['color']} {llm['name']}</b><br>
                <small style="color:#6b7280">{llm['desc']}</small><br><br>
                <small>📏 {llm['context_limit']:,} tokens</small><br>
                {"<small>💰 $"+str(llm['cost_per_1k'])+"/1k tokens</small><br>" if llm['cost_per_1k'] else ""}
                <br><small><b>Strengths:</b><br>{'<br>'.join('• '+s for s in llm['strengths'][:3])}</small>
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
        bg     = "#eef2ff" if selected else "#f9fafb"
        border = "2px solid #6366f1" if selected else "1px solid #e5e7eb"
        st.markdown(
            f"""<div style="border:{border};border-radius:12px;padding:20px;background:{bg};margin-bottom:12px;">
            <b>{'✅ ' if selected else ''}{level['title']}</b><br>
            <span style="color:#6b7280">{level['desc']}</span><br><br>
            {''.join(f"<span style='background:#e0e7ff;border-radius:4px;padding:2px 8px;margin-right:6px;font-size:12px'>{f}</span>" for f in level['features'])}
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
        g_border = "2px solid #6366f1" if g_selected else "1px solid #e5e7eb"
        st.markdown(
            f"""<div style="border:{g_border};border-radius:12px;padding:24px;background:{'#eef2ff' if g_selected else '#fff'};text-align:center;">
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
        e_border = "2px solid #6366f1" if e_selected else "1px solid #e5e7eb"
        st.markdown(
            f"""<div style="border:{e_border};border-radius:12px;padding:24px;background:{'#eef2ff' if e_selected else '#fff'};text-align:center;">
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
                background:#f9fafb;border:1px solid #e5e7eb;">
                <div style="font-size:3rem;font-weight:bold;color:{clr}">{score}%</div>
                <div style="color:#6b7280">{'🌟 Excellent!' if score>=85 else '👍 Good' if score>=70 else '⚠️ Needs work'}</div>
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
