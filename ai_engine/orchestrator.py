import logging
import time
from typing import Any, Dict, Optional

from .llm_client import ResilientLLMManager
from .prompts.bullet_improvement import render_bullet_improvement_prompt
from .prompts.career_feedback import render_career_feedback_prompt
from .prompts.contextual_analysis import render_contextual_prompt
from .prompts.skill_gap import render_skill_gap_prompt

logger = logging.getLogger("ResumeIQ.AIEngine.Orchestrator")


class AIResumeOrchestrator:
    """Coordinates execution of modular Prompt Engineering layers for ResumeIQ:
    - Module A: Contextual Resume Analysis
    - Module B: Intelligent Skill Gap Analysis
    - Module C: AI Resume Improvement Suggestions
    - Module D: Personalized Career Feedback

    Preserves separation between the ML statistical model and qualitative LLM outputs.
    """

    def __init__(self, prompt_version: str = "final"):
        self.llm_manager = ResilientLLMManager()
        self.prompt_version = prompt_version
        logger.info(f"AIResumeOrchestrator initialized with provider '{self.llm_manager.provider_name}' and prompt version '{prompt_version}'.")

    def _prepare_context(
        self,
        resume_data: Dict[str, Any],
        role: str,
        job_description: Optional[str] = None,
        ml_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Sanitizes and prepares context variables for prompt templates."""
        jd_clean = (job_description or "").strip()
        if not jd_clean:
            jd_clean = f"Standard industry benchmark qualifications for a {role} professional."

        # Format experience
        exp_list = resume_data.get("experience", [])
        if isinstance(exp_list, list) and exp_list:
            exp_text = "\n- ".join(exp_list)
        elif isinstance(exp_list, str) and exp_list:
            exp_text = exp_list
        else:
            exp_text = "No work experience entries extracted."

        # Format projects
        proj_list = resume_data.get("projects", [])
        if isinstance(proj_list, list) and proj_list:
            proj_text = "\n- ".join(proj_list)
        elif isinstance(proj_list, str) and proj_list:
            proj_text = proj_list
        else:
            proj_text = "No project entries extracted."

        # Format skills
        skills_list = resume_data.get("skills", [])
        if isinstance(skills_list, list) and skills_list:
            skills_text = ", ".join(skills_list)
        elif isinstance(skills_list, str) and skills_list:
            skills_text = skills_list
        else:
            skills_text = "No technical skills extracted."

        # Combine experience and projects for skill context
        exp_and_proj = f"EXPERIENCE:\n{exp_text}\n\nPROJECTS:\n{proj_text}"

        ml_pred = "Unknown"
        ml_score = 0
        if ml_results:
            ml_pred = ml_results.get("predicted_role", ml_pred)
            ml_score = ml_results.get("total_score", ml_score)

        return {
            "role": role,
            "job_description": jd_clean,
            "resume_text": resume_data.get("raw_text", ""),
            "experience_text": exp_text,
            "projects_text": proj_text,
            "skills_text": skills_text,
            "experience_and_projects": exp_and_proj,
            "experience": exp_list,
            "projects": proj_list,
            "ml_predicted_role": ml_pred,
            "ml_score": ml_score
        }

    def analyze(
        self,
        resume_data: Dict[str, Any],
        role: str,
        job_description: Optional[str] = None,
        ml_results: Optional[Dict[str, Any]] = None,
        version_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes the 4 modular AI evaluation layers in sequence.
        Returns a structured dictionary ready for frontend consumption.
        """
        start_time = time.time()
        v = version_override or self.prompt_version
        context = self._prepare_context(resume_data, role, job_description, ml_results)

        # -------------------------------------------------------------
        # Module A: Contextual Resume Analysis
        # -------------------------------------------------------------
        prompt_a = render_contextual_prompt(version=v, **context)
        ok_a, res_a, err_a = self.llm_manager.execute_prompt(prompt_a)

        # -------------------------------------------------------------
        # Module B: Intelligent Skill Gap Analysis
        # -------------------------------------------------------------
        prompt_b = render_skill_gap_prompt(version=v, **context)
        ok_b, res_b, err_b = self.llm_manager.execute_prompt(prompt_b)

        # -------------------------------------------------------------
        # Module C: AI Resume Improvement Suggestions
        # -------------------------------------------------------------
        prompt_c = render_bullet_improvement_prompt(version=v, **context)
        ok_c, res_c, err_c = self.llm_manager.execute_prompt(prompt_c)

        # -------------------------------------------------------------
        # Module D: Personalized Career Feedback
        # -------------------------------------------------------------
        prompt_d = render_career_feedback_prompt(version=v, **context)
        ok_d, res_d, err_d = self.llm_manager.execute_prompt(prompt_d)

        duration_sec = round(time.time() - start_time, 2)

        return {
            "status": "success",
            "provider": self.llm_manager.provider_name,
            "prompt_version": v,
            "duration_seconds": duration_sec,
            "job_description_provided": bool(job_description and job_description.strip()),
            "modules": {
                "contextual_analysis": res_a,
                "skill_gap_analysis": res_b,
                "bullet_improvement": res_c,
                "career_feedback": res_d
            },
            "execution_notes": {
                "module_a_notes": err_a or "Executed cleanly",
                "module_b_notes": err_b or "Executed cleanly",
                "module_c_notes": err_c or "Executed cleanly",
                "module_d_notes": err_d or "Executed cleanly"
            }
        }
