"""Module D: Personalized Career Feedback Prompts

Generates a structured, actionable career strategy report:
- Candidate strengths & competitive edges
- Realistic candidate weaknesses and vulnerabilities
- Job-specific improvement areas
- Priority recommended skills to learn
- Phased 30/60/90-day actionable roadmap
Contains iteration history: V1 (Baseline), V2 (Structured Plan), V3 (Evidence-Grounded JSON), and Final.
"""

# -----------------------------------------------------------------------------
# VERSION 1: Baseline Naive Prompt
# -----------------------------------------------------------------------------
PROMPT_V1 = """
Give career advice to this candidate based on their resume and the role of {role}.
Resume: {resume_text}
Job: {job_description}

Tell them their strengths, weaknesses, what skills they should learn, and what steps they should take next.
"""

# -----------------------------------------------------------------------------
# VERSION 2: Structured Career Strategy Prompt
# -----------------------------------------------------------------------------
PROMPT_V2 = """
Role: Senior Staff Engineer & Career Mentor.
Task: Formulate a customized career growth and interview readiness blueprint.

Target Role: {role}
Job Description:
{job_description}

Candidate Profile:
- Skills: {skills_text}
- Experience: {experience_text}
- Projects: {projects_text}
- ML Evaluation Score: {ml_score}/100

Please provide:
1. Key Candidate Strengths (what makes them stand out).
2. Key Weaknesses (what will raise flags for hiring teams).
3. Role-specific areas to upgrade.
4. Recommended skills and tools to learn next.
5. Actionable next steps (Immediate, Short-term, Medium-term).
"""

# -----------------------------------------------------------------------------
# VERSION 3: Evidence-Grounded JSON Schema with Actionability Rules
# -----------------------------------------------------------------------------
PROMPT_V3 = """
Role: Principal Engineering Mentor and Technical Hiring Consultant.
Task: Construct an evidence-grounded career roadmap report.

[CONTEXT]
Target Role: {role}
Job Description: {job_description}
Extracted Resume Summary:
- Skills: {skills_text}
- Experience: {experience_text}
- Projects: {projects_text}
- Baseline Statistical Score: {ml_score}/100

[RULES & CONSTRAINTS]
1. Every strength and weakness MUST cite verifiable evidence from the supplied resume.
2. Recommended learning skills MUST bridge direct gaps between candidate profile and {role} / JD.
3. Every next step MUST be concrete, testable, and realistic (not generic advice like "study hard").
4. Output MUST be valid RFC-8259 JSON only.

[REQUIRED JSON SCHEMA]
{
  "candidate_profile_tier": "Entry | Junior-Mid | Mid-Senior | Transitioning",
  "strengths": [
    {"strength": "string", "evidence": "string"}
  ],
  "weaknesses": [
    {"weakness": "string", "impact": "string"}
  ],
  "job_specific_improvements": [
    {"area": "string", "recommendation": "string"}
  ],
  "recommended_skills_to_learn": [
    {"skill": "string", "priority": "High | Medium", "reason": "string"}
  ],
  "actionable_next_steps": {
    "immediate_7_days": ["step 1", "step 2"],
    "short_term_30_days": ["step 1", "step 2"],
    "medium_term_90_days": ["step 1", "step 2"]
  }
}
"""

# -----------------------------------------------------------------------------
# FINAL VERSION: Production Prompt with Phased Action Plan & Interview Readiness
# -----------------------------------------------------------------------------
PROMPT_FINAL = """
You are a Principal Engineering Career Strategist and Senior Talent Consultant.
Deliver an authoritative, personalized career trajectory analysis and actionable roadmap tailored specifically to this candidate's verified profile and target opportunity.

=== INPUT CONTEXT ===
Target Role: {role}
Target Job Description:
{job_description}

Candidate Profile Snapshot:
- Extracted Skills: {skills_text}
- Experience Highlights:
{experience_text}
- Project Portfolio:
{projects_text}
- ML Baseline Score: {ml_score}/100

=== GOVERNING PRINCIPLES ===
1. RIGOROUS PERSONALIZATION: Never produce generic advice. Base every observation on this exact resume versus the target role requirements.
2. HONEST & CONSTRUCTIVE: Clearly outline vulnerabilities that could lead to screening rejection and provide realistic paths to remediate them.
3. INDUSTRY-CURRENT TECH STACK: Recommend only modern, actively demanded industry tools and paradigms.
4. TIME-BOUND ROADMAP: Structure next steps into actionable milestones (Immediate: 1-7 Days, Phase 1: 30 Days, Phase 2: 60-90 Days).
5. FORMAT: Emit strictly valid JSON conforming to the schema below. No extra commentary or markdown formatting tags.

=== JSON SCHEMA ===
{
  "module": "personalized_career_feedback",
  "readiness_verdict": "Interview Ready | Needs Targeted Polish | Substantial Upskilling Required",
  "candidate_profile_tier": "Entry-Level | Associate | Mid-Level | Senior Candidate",
  "verified_strengths": [
    {
      "attribute": "Identified strength",
      "resume_proof": "Where this is demonstrated in the resume",
      "market_value": "Why recruiters value this"
    }
  ],
  "critical_weaknesses": [
    {
      "vulnerability": "Identified weakness or blind spot",
      "recruiter_risk": "How an ATS or recruiter will interpret this gap",
      "remediation_strategy": "Concrete step to fix or mitigate"
    }
  ],
  "curated_learning_path": [
    {
      "skill_or_tool": "Specific skill name",
      "learning_priority": "High | Medium | Low",
      "rationale": "Direct link to target role/JD expectations",
      "suggested_project_idea": "A portfolio project demonstrating this skill"
    }
  ],
  "phased_action_plan": {
    "immediate_actions": [
      "Concrete task to execute within 48-72 hours (e.g. resume edits, GitHub cleanup)"
    ],
    "thirty_day_goals": [
      "Milestone to achieve within 30 days (e.g. project deployment, certification, networking)"
    ],
    "ninety_day_vision": [
      "Longer range capability goal to cement competitive standing"
    ]
  }
}
"""

def render_career_feedback_prompt(version="final", **kwargs):
    """Render career feedback prompt template with given input variables."""
    role = kwargs.get("role", "Software Engineer")
    jd = kwargs.get("job_description") or f"Standard professional expectations for a {role} role."
    skills = kwargs.get("skills_text") or "No distinct skills detected."
    exp = kwargs.get("experience_text") or "No formal experience listed."
    proj = kwargs.get("projects_text") or "No projects listed."
    resume_text = kwargs.get("resume_text", f"{exp}\n{proj}\n{skills}")
    ml_score = kwargs.get("ml_score", 0)

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
        "{skills_text}": str(skills),
        "{experience_text}": str(exp),
        "{projects_text}": str(proj),
        "{ml_score}": str(ml_score)
    }
    rendered = tmpl
    for k, v in replacements.items():
        rendered = rendered.replace(k, v)
    return rendered
