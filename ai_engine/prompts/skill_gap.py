"""Module B: Intelligent Skill Gap Analysis Prompts

Identifies required skills, demonstrated skills with evidence, missing skills,
partially demonstrated skills, and transferable skills between resume and JD.
Contains iteration history: V1 (Baseline), V2 (Structured Categories), V3 (Evidence-Constrained), and Final.
"""

# -----------------------------------------------------------------------------
# VERSION 1: Baseline Naive Prompt
# -----------------------------------------------------------------------------
PROMPT_V1 = """
Find the skill gaps between this resume and this job description.
Resume skills: {skills_text}
Resume text: {resume_text}
Job description: {job_description}
Target role: {role}

List the skills required, skills the candidate has, skills they are missing, and what they can transfer.
"""

# -----------------------------------------------------------------------------
# VERSION 2: Structured Categorization Prompt
# -----------------------------------------------------------------------------
PROMPT_V2 = """
Role: Senior Technical Talent Evaluator.
Task: Analyze the technical and soft skill gaps between the candidate's resume and the job description.

Target Role: {role}
Job Description:
{job_description}

Extracted Resume Skills:
{skills_text}

Full Resume Context:
{resume_text}

Please provide:
1. Skills explicitly demanded by the Job Description.
2. Skills clearly proven in the resume.
3. Critical missing skills that the candidate must acquire.
4. Partially demonstrated skills (mentioned but no deep project proof).
5. Transferable skills from their background.

Format as a clear bulleted report.
"""

# -----------------------------------------------------------------------------
# VERSION 3: Evidence-Enforced Structured JSON Prompt
# -----------------------------------------------------------------------------
PROMPT_V3 = """
Role: Lead Technical Interviewer and Skills Assessor.
Task: Perform a strict, evidence-based skill gap audit between the Job Description and Candidate Profile.

[INPUT CONTEXT]
Target Role: {role}
Job Description:
{job_description}

Extracted Candidate Skills:
{skills_text}

Candidate Work Experience & Projects:
{experience_and_projects}

[STRICT EVIDENCE CONSTRAINTS]
1. ZERO ASSUMPTIONS: You must NEVER mark a skill as 'demonstrated' unless there is explicit textual proof (code, framework, duty, or artifact) in the resume.
2. If a skill appears only in a keyword list without any contextual usage, classify it as 'partially_demonstrated'.
3. 'transferable_skills' must explain the concrete bridge (e.g., C++ experience bridging to Java OOP concepts).
4. Output MUST be valid RFC-8259 JSON only.

[REQUIRED JSON SCHEMA]
{
  "skills_required_by_jd": ["skill1", "skill2"],
  "skills_demonstrated": [
    {
      "skill": "skill_name",
      "evidence_in_resume": "quote or specific project where applied"
    }
  ],
  "missing_skills": [
    {
      "skill": "skill_name",
      "importance": "Critical" | "Secondary",
      "reason": "why this skill is necessary for this role"
    }
  ],
  "partially_demonstrated_skills": [
    {
      "skill": "skill_name",
      "status": "Keyword listed only with no project context / Coursework only",
      "recommendation_to_prove": "how candidate can substantiate it"
    }
  ],
  "transferable_skills": [
    {
      "existing_skill": "skill candidate already has",
      "maps_to_target": "target required skill",
      "transferability_rationale": "why this prior experience helps"
    }
  ]
}
"""

# -----------------------------------------------------------------------------
# FINAL VERSION: Production Prompt with Fallbacks, Match Index & Anti-Hallucination
# -----------------------------------------------------------------------------
PROMPT_FINAL = """
You are an expert AI Competency Architect and Technical Skills Evaluator.
Your task is to conduct an authoritative, rigorous skill gap breakdown comparing a candidate's resume evidence against a target role and Job Description.

=== INPUT DATA ===
Target Job Role: {role}
Target Job Description:
{job_description}

Candidate Skills:
{skills_text}

Candidate Experience & Project Descriptions:
{experience_and_projects}

=== CRITICAL EVALUATION RULES ===
1. EVIDENCE BOUNDARY: Never credit a skill as demonstrated without citation of the specific line or project context where it was utilized.
2. DISTINCTION BETWEEN LISTED VS DEMONSTRATED:
   - "demonstrated": Used in actual work, project, or quantifiable accomplishment.
   - "partially_demonstrated": Listed in a skills bank or course list, but without descriptive proof of application.
   - "missing": Demanded by the role/JD and completely absent from the resume.
   - "transferable": A skill the candidate provenly possesses that directly accelerates proficiency in a missing target skill.
3. DEFAULT ROBUSTNESS: If the Job Description is sparse or absent, extract required skills from current industry hiring standards for '{role}'.
4. FORMAT: Return exclusively valid JSON conforming strictly to the schema below. No Markdown code fence backticks around the json.

=== JSON SCHEMA ===
{
  "module": "intelligent_skill_gap_analysis",
  "match_percentage": 0-100 integer representing percentage of critical JD skills satisfied,
  "summary": "Concise 2-sentence summary of the candidate's skill preparedness.",
  "skills_required_by_jd": [
    "Explicitly required skill name"
  ],
  "demonstrated_skills": [
    {
      "skill": "skill_name",
      "evidence": "Direct quote or description of where demonstrated in resume",
      "proficiency_signal": "Basic | Intermediate | Advanced"
    }
  ],
  "missing_skills": [
    {
      "skill": "missing_skill_name",
      "severity": "High | Medium | Low",
      "impact_on_hiring": "Why this creates friction during screening"
    }
  ],
  "partially_demonstrated_skills": [
    {
      "skill": "skill_name",
      "current_gap": "e.g., Listed in skills list but omitted from project tech stacks",
      "action_to_validate": "Specific project enhancement or bullet point needed to prove competency"
    }
  ],
  "transferable_skills": [
    {
      "candidate_skill": "Known candidate skill",
      "target_skill": "Missing or desired target skill",
      "bridge_rationale": "Clear technical explanation of how skill A translates to skill B"
    }
  ]
}
"""

def render_skill_gap_prompt(version="final", **kwargs):
    """Render skill gap prompt template with given input variables."""
    role = kwargs.get("role", "Software Engineer")
    jd = kwargs.get("job_description") or f"Standard professional expectations for a {role} position."
    skills = kwargs.get("skills_text") or "No distinct skills detected."
    exp_proj = kwargs.get("experience_and_projects") or kwargs.get("resume_text", "No experience or projects provided.")
    resume_text = kwargs.get("resume_text", exp_proj)

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
        "{skills_text}": str(skills),
        "{experience_and_projects}": str(exp_proj),
        "{resume_text}": str(resume_text)
    }
    rendered = tmpl
    for k, v in replacements.items():
        rendered = rendered.replace(k, v)
    return rendered
