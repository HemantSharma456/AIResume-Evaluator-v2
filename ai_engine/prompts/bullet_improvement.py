"""Module C: AI Resume Improvement Suggestions Prompts

Analyzes bullet points from experience and projects, identifies weaknesses (passive voice,
lack of metrics, vague responsibilities), and generates high-impact rewrites adhering
to the Google XYZ formula (Accomplished [X] as measured by [Y], by doing [Z]).
NEVER fabricates employment history, achievements, qualifications, or metrics.
"""

# -----------------------------------------------------------------------------
# VERSION 1: Baseline Naive Prompt
# -----------------------------------------------------------------------------
PROMPT_V1 = """
Improve the following resume bullet points:
{bullets_text}
Make them sound better, more professional, and add numbers to make them impressive for a {role} role.
"""

# -----------------------------------------------------------------------------
# VERSION 2: Structured XYZ Framework Prompt
# -----------------------------------------------------------------------------
PROMPT_V2 = """
Role: Professional Executive Resume Writer & Career Coach.
Task: Critique and rewrite the candidate's experience and project bullets for a {role} position.

Target Role: {role}
Target Job Requirements: {job_description}

Input Bullet Points:
{bullets_text}

Instructions:
1. Identify bullet points that are weak, passive, or lack measurable business impact.
2. Rewrite each weak bullet using the Google XYZ format: "Accomplished [X], as measured by [Y], by doing [Z]".
3. Do not invent fake statistics; use bracketed placeholders like "[improved query latency by X%]" so the user can insert real numbers.
4. Suggest stronger action verbs and industry-standard terminology.
5. Provide recommendations to elevate project descriptions.
"""

# -----------------------------------------------------------------------------
# VERSION 3: Strict JSON Schema with Anti-Fabrication Safeguards
# -----------------------------------------------------------------------------
PROMPT_V3 = """
Role: ATS Optimization Architect and Executive Resume Consultant.
Task: Generate targeted, non-hallucinatory bullet point and project improvements.

[CONTEXT]
Target Role: {role}
Job Description: {job_description}

Original Resume Bullets & Descriptions:
{bullets_text}

[STRICT ETHICAL & ACCURACY CONSTRAINTS]
1. ZERO FABRICATION: Never fabricate past employers, job titles, technologies unmentioned by candidate, or fictitious quantitative results.
2. Use explicit prompt templates/placeholders (e.g., "[reduced response latency by ~X%]", "[scaled to handle N concurrent requests]") indicating where candidate must supply their verified figures.
3. Every suggestion MUST preserve the factual core of the original bullet.
4. Output MUST be valid RFC-8259 JSON only.

[REQUIRED JSON SCHEMA]
{
  "total_bullets_analyzed": integer,
  "bullet_improvements": [
    {
      "original_text": "string",
      "detected_weakness": "e.g. Passive voice, lack of metric, vague scope",
      "suggested_rewrite": "string with [X] metrics placeholder",
      "action_verb_used": "string",
      "framework_applied": "XYZ | STAR",
      "expected_impact": "string"
    }
  ],
  "project_enhancements": [
    {
      "project_title": "string",
      "critique": "string",
      "enhancement_guidance": "string"
    }
  ],
  "missing_critical_details": ["detail 1", "detail 2"]
}
"""

# -----------------------------------------------------------------------------
# FINAL VERSION: Production Prompt with Dual Rewrites & Before/After Contrast
# -----------------------------------------------------------------------------
PROMPT_FINAL = """
You are a elite Technical Resume Specialist and ATS Optimization Engineer.
Your objective is to diagnose weaknesses in a candidate's resume bullet points and provide surgical, high-impact transformations strictly grounded in truth.

=== INPUT CONTEXT ===
Target Role: {role}
Target Job Description:
{job_description}

Original Candidate Bullet Points / Project Descriptions:
{bullets_text}

=== ANTI-HALLUCINATION & INTEGRITY DIRECTIVES ===
1. ABSOLUTE TRUTHFULNESS: Never invent achievements, awards, credentials, or arbitrary performance figures.
2. TRANSPARENT METRIC SLOTS: Where quantification is needed, use bracketed guide slots like "[by ~X% (insert your real metric)]" or "[supporting ~N daily active users]".
3. PRESERVE INTENT: Every rewrite must remain a faithful upgrade of the candidate's actual work, elevating passive wording into active leadership and technical precision.
4. REFORMATTING STANDARD: Format each rewrite using the Google XYZ standard: "Accomplished [X], as measured by [Y], by doing [Z]".
5. OUTPUT: Output ONLY a single, valid JSON object without surrounding prose or markdown fences.

=== JSON SCHEMA ===
{
  "module": "resume_improvement_suggestions",
  "audit_summary": "1-2 sentence assessment of bullet quality, action verb strength, and ATS readability.",
  "bullet_transformations": [
    {
      "original_bullet": "Exact quote from resume",
      "weakness_type": "Passive Voice | Missing Quantification | Vague Tech Stack | Task-Only Description",
      "critique": "Specific diagnosis of why this underperforms in recruiter review",
      "optimized_rewrite": "Action-verb led rewrite with bracketed [metric slot]",
      "action_verb": "Primary power verb used",
      "rationale": "Why this version ranks higher with hiring managers"
    }
  ],
  "critical_missing_elements": [
    "Concrete element missing (e.g. live link, unit testing mention, CI/CD pipeline, system metrics)"
  ]
}
"""

def render_bullet_improvement_prompt(version="final", **kwargs):
    """Render bullet improvement prompt template with given input variables."""
    role = kwargs.get("role", "Software Engineer")
    jd = kwargs.get("job_description") or f"Standard expectations for {role}."
    
    # Extract bullets from experience, projects, or summary
    bullets = kwargs.get("bullets_text")
    if not bullets:
        exp = kwargs.get("experience", [])
        proj = kwargs.get("projects", [])
        combined = []
        if isinstance(exp, list):
            combined.extend(exp)
        elif isinstance(exp, str) and exp:
            combined.append(exp)
        if isinstance(proj, list):
            combined.extend(proj)
        elif isinstance(proj, str) and proj:
            combined.append(proj)
        bullets = "\n- ".join(combined) if combined else "No explicit experience or project bullets provided."
        if not bullets.startswith("- "):
            bullets = f"- {bullets}"

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
        "{bullets_text}": str(bullets)
    }
    rendered = tmpl
    for k, v in replacements.items():
        rendered = rendered.replace(k, v)
    return rendered
