"""Module A: Contextual Resume Analysis Prompts

Evaluates the candidate's resume relative to a target role and specific Job Description (JD).
Contains iteration history: V1 (Baseline), V2 (Structured Context), V3 (Constrained Schema), and Final.
"""

# -----------------------------------------------------------------------------
# VERSION 1: Baseline Naive Prompt
# -----------------------------------------------------------------------------
PROMPT_V1 = """
You are a resume reviewer. Review this resume for the role of {role} and the following job description:
{job_description}

Resume:
{resume_text}

Tell me how well the candidate matches the job, what projects are relevant, their strengths, and what they need to improve.
"""

# -----------------------------------------------------------------------------
# VERSION 2: Structured Context & Role Definition
# -----------------------------------------------------------------------------
PROMPT_V2 = """
Role: Senior Technical Recruiter & Hiring Manager.
Task: Perform a contextual analysis of the candidate's resume against the target role and provided Job Description.

Target Role: {role}
Target Job Description:
{job_description}

Extracted Candidate Information:
- Experience: {experience_text}
- Projects: {projects_text}
- Skills: {skills_text}
- Existing ML Match Prediction: {ml_predicted_role} (Score: {ml_score}/100)

Instructions:
1. Assess the candidate's total experience and seniority alignment.
2. Identify which specific projects demonstrate direct relevance to the job requirements.
3. Identify top 3 candidate strengths.
4. Identify 3 areas needing immediate improvement.
5. Provide an alignment rating: Strong, Moderate, or Weak.

Return your response in clean markdown.
"""

# -----------------------------------------------------------------------------
# VERSION 3: Strict JSON Schema with Hallucination Constraints
# -----------------------------------------------------------------------------
PROMPT_V3 = """
Role: Senior Technical Recruiter and ATS Specialist.
Task: Conduct a rigorous contextual evaluation of the candidate's resume against the Job Description.

[INPUT CONTEXT]
Target Role: {role}
Job Description:
{job_description}

Candidate Profile:
- Relevant Experience:
{experience_text}
- Projects:
{projects_text}
- Skills Extracted:
{skills_text}
- ML Baseline: Predicted Role = {ml_predicted_role}, Model Score = {ml_score}/100

[CONSTRAINTS]
1. Base all judgments STRICTLY on evidence present in the candidate profile. Do not invent details.
2. If the Job Description is empty or generic, evaluate against standard industry expectations for '{role}'.
3. Output MUST be valid RFC-8259 JSON only. No prose outside the JSON object.

[REQUIRED JSON OUTPUT FORMAT]
{
  "role_alignment_rating": "High" | "Moderate" | "Low",
  "alignment_summary": "2-3 sentences evaluating overall role & JD fit based on verifiable evidence",
  "experience_relevance": {
    "verdict": "string",
    "years_demonstrated_summary": "string",
    "key_alignment_points": ["point 1", "point 2"]
  },
  "relevant_projects": [
    {
      "project_title": "string",
      "relevance_explanation": "how this project addresses JD requirements",
      "technologies_matched": ["tech1", "tech2"]
    }
  ],
  "candidate_strengths": ["strength 1 with resume evidence", "strength 2 with resume evidence"],
  "areas_for_improvement": ["area 1 tied to JD gaps", "area 2 tied to JD gaps"]
}
"""

# -----------------------------------------------------------------------------
# FINAL VERSION: Production Prompt with Chain-of-Thought Grounding & Edge-Case Guards
# -----------------------------------------------------------------------------
PROMPT_FINAL = """
You are an expert AI Technical Recruiter and Career Strategist.
Your objective is to perform an objective, evidence-grounded contextual analysis comparing a candidate's parsed resume against a target role and Job Description (JD).

=== INPUT CONTEXT ===
Target Role: {role}
Job Description (JD):
{job_description}

Candidate Parsed Resume Data:
- Experience Summary:
{experience_text}
- Projects:
{projects_text}
- Extracted Skills:
{skills_text}
- Statistical ML Baseline:
  * Predicted Role: {ml_predicted_role}
  * Benchmark Score: {ml_score}/100

=== OPERATIONAL CONSTRAINTS & RULES ===
1. ZERO-HALLUCINATION POLICY: Cite only tools, responsibilities, and achievements explicitly mentioned in the candidate's text.
2. ABSENCE HANDLING: If the Job Description is not provided or says 'Not specified', formulate the evaluation using canonical senior expectations for the '{role}' role.
3. CONFLICT HANDLING: If the candidate claims a skill but lists no project or experience applying it, classify it as claimed without applied depth.
4. OUTPUT SPECIFICATION: Output MUST be a single, valid, parsable JSON object. Never wrap in markdown commentary or backticks.

=== REQUIRED JSON SCHEMA ===
{
  "module": "contextual_resume_analysis",
  "role_alignment_rating": "High | Moderate | Low | Poor",
  "alignment_score_estimate": 0-100 integer representing semantic alignment to JD,
  "executive_summary": "Concise 2-3 sentence executive evaluation grounded in facts.",
  "experience_alignment": {
    "seniority_fit": "Junior | Mid-Level | Senior | Lead | Mismatched",
    "analysis": "Detailed objective assessment of demonstrated responsibilities.",
    "direct_matches": ["List of responsibilities directly matching JD needs"]
  },
  "relevant_projects": [
    {
      "project_title": "Identified project name or descriptor",
      "relevance_explanation": "Concrete reason this project proves capability for the JD",
      "demonstrated_tools": ["tool1", "tool2"]
    }
  ],
  "verified_strengths": [
    "Strength 1 with explicit evidence from resume",
    "Strength 2 with explicit evidence from resume"
  ],
  "critical_gaps": [
    "Clear actionable gap between resume evidence and JD expectations"
  ]
}
"""

def render_contextual_prompt(version="final", **kwargs):
    """Render prompt template with given input variables."""
    role = kwargs.get("role", "Software Engineer")
    jd = kwargs.get("job_description") or "Not specified. Evaluate based on standard industry expectations for the role."
    exp = kwargs.get("experience_text") or "No formal work experience listed in resume."
    proj = kwargs.get("projects_text") or "No distinct projects listed."
    skills = kwargs.get("skills_text") or "No skills extracted."
    ml_predicted = kwargs.get("ml_predicted_role", "Unknown")
    ml_score = kwargs.get("ml_score", 0)
    resume_text = kwargs.get("resume_text", f"{exp}\n{proj}\n{skills}")

    prompts = {
        "v1": PROMPT_V1,
        "v2": PROMPT_V2,
        "v3": PROMPT_V3,
        "final": PROMPT_FINAL
    }
    tmpl = prompts.get(version.lower(), PROMPT_FINAL)
    replacements = {
        "{role}": str(role),
        "{job_description}": str(jd),
        "{resume_text}": str(resume_text),
        "{experience_text}": str(exp),
        "{projects_text}": str(proj),
        "{skills_text}": str(skills),
        "{ml_predicted_role}": str(ml_predicted),
        "{ml_score}": str(ml_score)
    }
    rendered = tmpl
    for k, v in replacements.items():
        rendered = rendered.replace(k, v)
    return rendered

