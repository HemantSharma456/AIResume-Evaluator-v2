from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from ml_model import ResumeEvaluator
from resume_parser import ResumeParser
from services.job_service import JobService
from ai_engine.orchestrator import AIResumeOrchestrator

load_dotenv()

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
UPLOAD_FOLDER = '/tmp/uploads' if IS_VERCEL else os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

evaluator = ResumeEvaluator()
parser = ResumeParser()
job_service = JobService()
ai_orchestrator = AIResumeOrchestrator()
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass

if not evaluator.load_model():
    print("Training new model...")
    evaluator.train(os.path.join(BASE_DIR, 'Dataset.csv'))
    evaluator.save_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index.html')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/roles', methods=['GET'])
def get_roles():
    return jsonify({'roles': ['Data Analyst', 'SDE(Frontend)', 'SDE(Backend)', 'SDE(Fullstack)']})

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files or not request.files['file'].filename:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        role = request.form.get('role', 'Data Analyst')
        job_description = request.form.get('job_description', '').strip()
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, DOC, TXT'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{filename}")
        file.save(file_path)
        
        resume_data = parser.parse_resume(file_path)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
        predicted_role, role_probs = evaluator.predict_role(resume_data['raw_text'])
        scores, max_scores = evaluator.calculate_section_scores(resume_data, role)
        
        total_score = sum(scores.values())
        max_total = sum(max_scores.values())
        
        suggestions = evaluator.generate_suggestions(resume_data, role, scores)
        suggestions_by_section = {}
        for s in suggestions:
            section = s['section']
            suggestions_by_section.setdefault(section, []).append(s)

        # Execute Modular AI Prompt Engineering Analysis Layer
        ai_analysis = ai_orchestrator.analyze(
            resume_data=resume_data,
            role=role,
            job_description=job_description,
            ml_results={
                'predicted_role': predicted_role,
                'total_score': round(total_score, 2),
                'scores': scores
            }
        )
        
        try:
            os.remove(file_path)
        except:
            pass
        return jsonify({
            'filename': filename,
            'role': role,
            'predicted_role': predicted_role,
            'role_match_probability': role_probs.get(role, 0),
            'total_score': round(total_score, 2),
            'max_score': max_total,
            'score_percentage': round((total_score / max_total * 100) if max_total > 0 else 0, 2),
            'scores': {k: round(v, 2) for k, v in scores.items()},
            'max_scores': max_scores,
            'resume_data': {k: resume_data[k] for k in ['basic_details', 'professional_summary', 
                                                         'education', 'experience', 'projects', 
                                                         'certification', 'skills']},
            'suggestions': suggestions_by_section,
            'ai_analysis': ai_analysis,
            'job_description_provided': bool(job_description)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/analyze', methods=['POST'])
def analyze_custom_ai():
    """Direct API endpoint for Prompt Engineering testing and re-analysis."""
    try:
        payload = request.get_json() or {}
        resume_text = payload.get('resume_text', '')
        role = payload.get('role', 'Data Analyst')
        job_description = payload.get('job_description', '')
        version = payload.get('version', 'final')

        # Use parser on the raw text
        resume_data = {
            'basic_details': parser.extract_basic_details(resume_text),
            'professional_summary': parser.extract_professional_summary(resume_text),
            'education': parser.extract_education(resume_text),
            'experience': parser.extract_experience(resume_text),
            'projects': parser.extract_projects(resume_text),
            'certification': parser.extract_certifications(resume_text),
            'skills': parser.extract_skills(resume_text),
            'raw_text': resume_text
        }
        scores, max_scores = evaluator.calculate_section_scores(resume_data, role)
        predicted_role, _ = evaluator.predict_role(resume_text) if evaluator.is_trained else (role, {})
        
        ai_res = ai_orchestrator.analyze(
            resume_data=resume_data,
            role=role,
            job_description=job_description,
            ml_results={'predicted_role': predicted_role, 'total_score': sum(scores.values())},
            version_override=version
        )
        return jsonify(ai_res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_trained': evaluator.is_trained,
        'ai_provider': ai_orchestrator.llm_manager.provider_name
    })


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    skills_query = request.args.get('skills', '').strip()
    try:
        jobs = job_service.get_recommendations(skills_query or 'software developer', limit=6)
        return jsonify({'jobs': jobs, 'adzuna_configured': True, 'count': len(jobs)})
    except Exception:
        jobs = job_service._generate_smart_recommendations(skills_query or 'software developer', limit=6)
        return jsonify({'jobs': jobs, 'adzuna_configured': True, 'count': len(jobs)})

if __name__ == '__main__':
    app.run(debug=True, port=4000)

