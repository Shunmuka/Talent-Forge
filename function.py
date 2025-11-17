import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import docx
import re

# === YOUR GEMINI API KEY (EDIT THIS LINE ONLY) ===
GEMINI_API_KEY = "AIzaSyBYPhIsuGYXzMRiYrFi7yw6M2bH3EB4TFA"

if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-api-key-here":
    st.error("Please set your Gemini API key in the code (line 9).")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# === LOAD EMBEDDER ===
@st.cache_resource
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedder = load_embedder()

# === CONFIG ===
st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("Resume to Job Matcher")

# === TEXT EXTRACTION ===
def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    return ""

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_bullets(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    bullets = []
    for line in lines:
        line = line.strip()
        # Match bullet starters or continuation lines
        if re.match(r'^[-•*]\s', line) or (len(line) > 20 and line[0].islower()):
            clean_bullet = re.sub(r'^[-•*\s]+', '', line).strip()
            if len(clean_bullet) > 15:
                bullets.append(clean_bullet)
    return bullets[:15]  # Limit to 15

def compute_match_score(resume, job):
    r_emb = embedder.encode(resume, convert_to_tensor=True)
    j_emb = embedder.encode(job, convert_to_tensor=True)
    sim = util.cos_sim(r_emb, j_emb)[0][0].item()
    return round(sim * 100, 1)

# === GEMINI: GAP ANALYSIS ===
def analyze_gaps(resume, job_desc):
    prompt = f"""
    Compare resume and job description. List 3–5 critical missing hard skills, tools, or experience in ONE sentence each.
    Format: - Missing: [sentence]

    Resume:
    {resume[:3000]}

    Job:
    {job_desc[:3000]}
    """
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        gaps = [line.replace('- Missing:', '').strip() for line in lines if '- Missing:' in line]
        return gaps[:5] or ["No major gaps."]
    except Exception as e:
        return [f"Error: {str(e)}"]

# === GEMINI: REWRITE BULLET ===
def rewrite_bullet(bullet, job_desc):
    prompt = f"""
    Rewrite this bullet to better match the job. Use strong action verbs, mirror job language, keep under 120 characters.

    Bullet: {bullet}
    Job: {job_desc[:1500]}

    Rewritten:
    """
    try:
        response = model.generate_content(prompt)
        rewritten = response.text.strip()
        return rewritten if len(rewritten) < 150 else rewritten[:140] + "..."
    except:
        return f"Improved: {bullet}"

# === UI: INPUTS ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    resume_input = st.radio("Input", ["Upload File", "Paste Text"], key="resume_source")
    resume_text = ""

    if resume_input == "Upload File":
        file = st.file_uploader("PDF, DOCX, TXT", type=["pdf", "docx", "txt"], key="resume_file")
        if file:
            resume_text = extract_text(file)
            st.success("Resume loaded!")
    else:
        resume_text = st.text_area("Paste your full resume here", height=250, key="resume_paste")

with col2:
    st.subheader("Job Description")
    job_desc = st.text_area("Paste the job description here", height=250, key="job_desc")

# === VALIDATION ===
if not resume_text.strip():
    st.info("Please provide your resume (upload or paste).")
    st.stop()
if not job_desc.strip():
    st.info("Please provide the job description.")
    st.stop()

resume_clean = clean_text(resume_text)
job_clean = clean_text(job_desc)

# === AUTO-EXTRACT BULLETS ===
auto_bullets = extract_bullets(resume_clean)

# === ALWAYS SHOW BULLET EDITOR ===
st.markdown("---")
st.subheader("✏️ Edit & Rewrite Bullet Points")

st.markdown("""
Enter or edit your resume bullet points below.  
We'll rewrite them to **perfectly match the job**.
""")

# Initialize session state for bullets
if 'user_bullets' not in st.session_state:
    st.session_state.user_bullets = auto_bullets or [""] * 5

# Allow user to set number of bullets
num_bullets = st.slider("Number of bullets to edit", 1, 15, min(5, len(st.session_state.user_bullets) or 5))
st.session_state.user_bullets = st.session_state.user_bullets[:num_bullets] + [""] * (num_bullets - len(st.session_state.user_bullets))

# Text areas for each bullet
bullets_to_rewrite = []
for i in range(num_bullets):
    default = st.session_state.user_bullets[i] if i < len(st.session_state.user_bullets) else ""
    bullet = st.text_area(
        f"Bullet {i+1}",
        value=default,
        height=80,
        key=f"bullet_{i}",
        help="Edit this bullet to be rewritten"
    )
    if bullet.strip():
        bullets_to_rewrite.append(bullet.strip())

# Update session state
st.session_state.user_bullets = [st.session_state[f"bullet_{i}"] for i in range(num_bullets)]

# === ANALYZE MATCH BUTTON ===
if st.button("🔍 Analyze Match & Gaps", type="primary"):
    with st.spinner("Analyzing resume and job match..."):
        score = compute_match_score(resume_clean, job_clean)
        gaps = analyze_gaps(resume_clean, job_clean)

    st.markdown("---")
    colA, colB = st.columns([1, 2])
    with colA:
        st.metric("Match Score", f"{score}/100")
        if score >= 80:
            st.success("Strong Match!")
        elif score >= 60:
            st.warning("Good, but can improve")
        else:
            st.error("Needs significant tailoring")
    with colB:
        st.markdown("### Critical Gaps")
        for gap in gaps:
            st.markdown(f"• {gap}")

# === REWRITE BULLETS BUTTON (Always Available) ===
if bullets_to_rewrite:
    if st.button("✨ Rewrite Bullets to Match Job", type="secondary"):
        with st.spinner(f"Rewriting {len(bullets_to_rewrite)} bullets..."):
            rewritten = []
            progress = st.progress(0)
            for i, bullet in enumerate(bullets_to_rewrite):
                new = rewrite_bullet(bullet, job_clean)
                rewritten.append((bullet, new))
                progress.progress((i + 1) / len(bullets_to_rewrite))
            progress.empty()

        st.markdown("### Tailored Bullet Points")
        download_text = ""
        for i, (orig, new) in enumerate(rewritten):
            with st.expander(f"Bullet {i+1}: {new[:60]}..."):
                st.markdown(f"**Original:** {orig}")
                st.markdown(f"**✨ Improved:** {new}")
            download_text += f"• {new}\n"

        st.download_button(
            "📥 Download Rewritten Bullets",
            download_text,
            "tailored_bullets.txt",
            "text/plain"
        )
else:
    st.info("Add at least one bullet point to rewrite.")

