from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import docx
import re
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "AIzaSyBYPhIsuGYXzMRiYrFi7yw6M2bH3EB4TFA")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-api-key-here":
    raise ValueError("Please set your Gemini API key")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Load embedder once at startup (cached in serverless environment)
embedder = None

def get_embedder():
    global embedder
    if embedder is None:
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return embedder


def extract_text(file):
    """Extract text from uploaded file"""
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext == 'pdf':
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    elif file_ext == 'docx':
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file_ext == 'txt':
        return file.read().decode('utf-8')
    return ""


def clean_text(text):
    """Clean and normalize text"""
    return re.sub(r'\s+', ' ', text).strip()


def extract_bullets(text):
    """Extract bullet points from resume text"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    bullets = []
    for line in lines:
        line = line.strip()
        if re.match(r'^[-•*]\s', line) or (len(line) > 20 and line[0].islower()):
            clean_bullet = re.sub(r'^[-•*\s]+', '', line).strip()
            if len(clean_bullet) > 15:
                bullets.append(clean_bullet)
    return bullets[:15]


def compute_match_score(resume, job):
    """Calculate semantic similarity score"""
    emb = get_embedder()
    r_emb = emb.encode(resume, convert_to_tensor=True)
    j_emb = emb.encode(job, convert_to_tensor=True)
    sim = util.cos_sim(r_emb, j_emb)[0][0].item()
    return round(sim * 100, 1)


def analyze_gaps(resume, job_desc):
    """Identify gaps between resume and job description"""
    prompt = f"""
    You are a resume expert. Compare the resume and job description below.
    
    Identify 3-5 critical gaps where the resume is missing important skills, tools, technologies, certifications, or experience mentioned in the job description.
    
    Format your response as a bulleted list with each gap on its own line starting with a dash or bullet point.
    Be specific and concise - one clear sentence per gap.
    
    Resume:
    {resume[:3000]}

    Job Description:
    {job_desc[:3000]}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        lines = text.split('\n')
        gaps = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                clean_line = re.sub(r'^[-•*]\s*', '', line).strip()
                if len(clean_line) > 10:
                    gaps.append(clean_line)
        
        if not gaps:
            gaps = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]
        
        return gaps[:5] if gaps else ["Unable to identify specific gaps. Consider reviewing job requirements manually."]
    except Exception as e:
        return [f"Error analyzing gaps: {str(e)}"]


def rewrite_bullet(bullet, job_desc):
    """Rewrite a single bullet point to match job description"""
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


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload"""
    try:
        file = request.files.get('resume_file')
        if file and file.filename:
            text = extract_text(file)
            bullets = extract_bullets(clean_text(text))
            return jsonify({
                'success': True,
                'text': text,
                'bullets': bullets
            })
        return jsonify({'success': False, 'error': 'No file uploaded'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume and job match"""
    try:
        data = request.json
        resume = clean_text(data.get('resume', ''))
        job_desc = clean_text(data.get('job_desc', ''))
        
        if not resume or not job_desc:
            return jsonify({'success': False, 'error': 'Missing resume or job description'})
        
        score = compute_match_score(resume, job_desc)
        gaps = analyze_gaps(resume, job_desc)
        
        return jsonify({
            'success': True,
            'score': score,
            'gaps': gaps
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/rewrite_bullets', methods=['POST'])
def rewrite_bullets():
    """Rewrite bullet points to match job"""
    try:
        data = request.json
        bullets = data.get('bullets', [])
        job_desc = clean_text(data.get('job_desc', ''))
        
        if not bullets or not job_desc:
            return jsonify({'success': False, 'error': 'Missing bullets or job description'})
        
        rewritten = []
        for bullet in bullets:
            if bullet.strip():
                new_bullet = rewrite_bullet(bullet.strip(), job_desc)
                rewritten.append({
                    'original': bullet,
                    'improved': new_bullet
                })
        
        return jsonify({
            'success': True,
            'rewritten': rewritten
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/download_bullets', methods=['POST'])
def download_bullets():
    """Generate downloadable text file of rewritten bullets"""
    try:
        data = request.json
        bullets = data.get('bullets', [])
        
        content = ""
        for bullet in bullets:
            content += f"• {bullet}\n"
        
        # Create in-memory file
        buffer = io.BytesIO()
        buffer.write(content.encode('utf-8'))
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name='tailored_bullets.txt',
            mimetype='text/plain'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# For Vercel serverless deployment
if __name__ == '__main__':
    app.run(debug=True, port=5000)
else:
    # This makes the app work with Vercel
    app = app