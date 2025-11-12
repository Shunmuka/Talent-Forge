import streamlit as st
from API_KEY import API_KEY
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import docx
import re

# === YOUR GEMINI API KEY (EDIT THIS LINE) ===
API_KEY = API_KEY  # ← PUT YOUR KEY HERE

if not API_KEY or API_KEY == "your-gemini-api-key-here":
    st.error("Set your Gemini API key on line 9.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# === LOAD EMBEDDER ===
@st.cache_resource
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

embedder = load_embedder()

# === CONFIG ===
st.set_page_config(page_title="Resume Analyzer + Rewriter", layout="wide")
st.title("Resume Analyzer & Bullet Rewriter (AI)")

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
        if re.match(r'^[-•*]\s', line) or (len(line) > 20 and not line[0].isupper()):
            clean_bullet = re.sub(r'^[-•*\s]+', '', line).strip()
            if len(clean_bullet) > 15:
                bullets.append(clean_bullet)
    return bullets[:20]

def compute_match_score(resume, job):
    r_emb = embedder.encode(resume, convert_to_tensor=True)
    j_emb = embedder.encode(job, convert_to_tensor=True)
    sim = util.cos_sim(r_emb, j_emb)[0][0].item()
    return round(sim * 100, 1)


def analyze_gaps(resume, job_desc):
    prompt = f"""
    You are a senior recruiter. Compare the resume and job description.

    Resume (first 3000 chars):
    {resume[:3000]}

    Job Description (first 3000 chars):
    {job_desc[:3000]}

    Return ONLY 3–5 short, one-sentence summaries of the MOST CRITICAL missing hard skills, tools, years of experience, or certifications.
    Focus only on what the candidate lacks.
    Format exactly:
    - Missing: [clear sentence]
    """
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        gaps = [line.replace('- Missing:', '').strip() for line in lines if '- Missing:' in line]
        return gaps[:5] or ["No major gaps detected."]
    except Exception as e:
        return [f"Error: {str(e)}"]

# === GEMINI: REWRITE BULLETS ===
def rewrite_bullets_with_gemini(bullet_text, job_desc):
    prompt = f"""
    Rewrite the following resume bullet points to perfectly match the job description.
    - Use strong action verbs
    - Mirror job language and keywords
    - Add impact/quantification if possible
    - Keep each under 120 characters
    - Return only the rewritten bullets, one per line

    Job Description:
    {job_desc[:2000]}

    Bullets to rewrite:
    {bullet_text}

    Rewritten:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# === UI ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    resume_input = st.radio("Input", ["Upload File", "Paste Text"], key="r")
    resume_text = ""

    if resume_input == "Upload File":
        file = st.file_uploader("PDF, DOCX, TXT", type=["pdf", "docx", "txt"])
        if file:
            resume_text = extract_text(file)
            st.success("Resume loaded!")
    else:
        resume_text = st.text_area("Paste resume", height=250)

with col2:
    st.subheader("Job Description")
    job_desc = st.text_area("Paste job description", height=250)

if not resume_text.strip() or not job_desc.strip():
    st.info("Upload or paste both resume and job description.")
    st.stop()

# === EXTRACT DATA ===
resume_clean = clean_text(resume_text)
job_clean = clean_text(job_desc)
bullets = extract_bullets(resume_clean)

# === SHOW GAPS ===
st.markdown("---")
st.markdown("### Critical Gaps (What You're Missing)")
gaps = analyze_gaps(resume_clean, job_clean)
for gap in gaps:
    st.markdown(f"• {gap}")

# === SHOW BULLETS ===
st.markdown("---")
st.markdown("### Bullet Points in Your Resume")
st.markdown("*Copy any you want to improve and paste below.*")
for i, bullet in enumerate(bullets):
    st.markdown(f"**{i+1}.** {bullet}")

# === TEXT BOX + REWRITE ===
st.markdown("---")
st.markdown("### Paste Bullets to Rewrite")
user_bullets = st.text_area(
    "Paste one or more bullet points (one per line):",
    height=150,
    placeholder="• Built web apps\n• Used Python"
)

if st.button("Rewrite with AI", type="primary"):
    if not user_bullets.strip():
        st.warning("Paste at least one bullet to rewrite.")
    else:
        with st.spinner("AI is rewriting..."):
            rewritten = rewrite_bullets_with_gemini(user_bullets.strip(), job_clean)
        st.markdown("### Rewritten Bullets")
        st.code(rewritten, language="text")
        st.download_button(
            "Download Rewritten Bullets",
            rewritten,
            "rewritten_bullets.txt",
            "text/plain"
        )

# === OPTIONAL: MATCH SCORE ===
with st.expander("Show Match Score"):
    score = compute_match_score(resume_clean, job_clean)
    st.metric("Resume ↔ Job Match", f"{score}/100")
    if score >= 80:
        st.success("Strong alignment!")
    elif score >= 60:
        st.warning("Good, but can improve.")
    else:
        st.error("Needs major tailoring.")

# Footer
st.caption("AI-Powered • Gaps + Bullets + Rewriting")