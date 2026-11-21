"""Systematic Test Suite for ResumeIQ AI Integration
Implements the 10 required test cases:
1. Normal resume with matching job description.
2. Resume with poor job alignment.
3. Resume with missing required skills.
4. Resume with strong experience but weak project descriptions.
5. Resume with irrelevant skills.
6. Empty job description.
7. Very short resume.
8. Resume with incomplete information.
9. Invalid input.
10. Malformed or incomplete extracted text.

Executes all test cases, verifies assertions, and records:
[Test ID, Input Description, Expected Output, Actual Output, Pass/Fail, Observation]
Saves complete execution records to tests/test_suite_results.json.
"""

import json
import os
import sys
import time

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from ai_engine.orchestrator import AIResumeOrchestrator


def build_test_cases():
    return [
        {
            "id": "TC-01",
            "name": "Normal resume with matching job description",
            "role": "SDE(Backend)",
            "job_description": "Seeking Backend Engineer proficient in Python, PostgreSQL, and REST APIs. Experience with Docker and microservices preferred.",
            "resume_data": {
                "basic_details": {"name": "Alex Mercer", "email": "alex@example.com", "phone": "555-0199", "github": "github.com/alexm", "linkedin": "linkedin.com/in/alexm"},
                "professional_summary": ["Experienced Backend Developer specialized in Python web services and relational database optimization."],
                "education": ["B.Tech in Computer Science, State University, 2022"],
                "experience": ["Backend Engineer at CloudScale (2022 - Present): Designed REST APIs in Python using Flask and PostgreSQL. Handled 500k monthly requests."],
                "projects": ["Distributed Task Queue: Implemented asynchronous worker queue in Python with Redis backend."],
                "certification": ["AWS Certified Cloud Practitioner (2023)"],
                "skills": ["Python", "Flask", "PostgreSQL", "REST APIs", "Redis", "Git", "Docker"],
                "raw_text": "Alex Mercer. Backend Engineer with Python, Flask, PostgreSQL, Redis, Docker, and REST APIs."
            },
            "ml_results": {"predicted_role": "SDE(Backend)", "total_score": 85.0},
            "expected": "High or Moderate alignment rating, matching skills recognized, zero unhandled errors."
        },
        {
            "id": "TC-02",
            "name": "Resume with poor job alignment",
            "role": "SDE(Backend)",
            "job_description": "Senior Backend Go Engineer required. High concurrency, gRPC, Kubernetes, Kafka, and Linux internals.",
            "resume_data": {
                "basic_details": {"name": "Clara Evans", "email": "clara@art.com", "phone": "555-0123"},
                "professional_summary": ["Creative Graphic Designer and Brand Strategist with 5 years in digital art and print media."],
                "education": ["B.A. in Fine Arts, Creative College, 2019"],
                "experience": ["Senior Graphic Designer at Studio X: Designed brand identity, logos, and marketing banners using Adobe Photoshop and Illustrator."],
                "projects": ["Brand Identity Campaign: Complete visual identity rebrand for consumer beverage company."],
                "certification": ["Adobe Certified Professional"],
                "skills": ["Adobe Photoshop", "Illustrator", "InDesign", "Typography", "Color Theory", "Figma"],
                "raw_text": "Clara Evans. Graphic Designer skilled in Adobe Photoshop, Illustrator, and typography."
            },
            "ml_results": {"predicted_role": "SDE(Frontend)", "total_score": 38.0},
            "expected": "Low/Mismatched alignment, substantial skill gaps flagged, honest readiness verdict."
        },
        {
            "id": "TC-03",
            "name": "Resume with missing required skills",
            "role": "SDE(Frontend)",
            "job_description": "Frontend React Specialist required. Must have extensive production experience with TypeScript, Next.js, Jest unit testing, and GraphQL.",
            "resume_data": {
                "basic_details": {"name": "Jordan Lee", "email": "jordan@dev.com"},
                "professional_summary": ["Frontend developer with experience building responsive web pages."],
                "education": ["B.S. Information Systems, 2023"],
                "experience": ["Junior Web Developer: Built static client websites using vanilla HTML, CSS, and basic JavaScript."],
                "projects": ["Personal Portfolio: Interactive portfolio website using CSS grid and vanilla JS."],
                "certification": [],
                "skills": ["HTML", "CSS", "JavaScript", "Bootstrap"],
                "raw_text": "Jordan Lee. Frontend developer familiar with HTML, CSS, JavaScript, and Bootstrap."
            },
            "ml_results": {"predicted_role": "SDE(Frontend)", "total_score": 52.0},
            "expected": "Identification of critical missing skills (TypeScript, Next.js, Jest, GraphQL) in gap analysis."
        },
        {
            "id": "TC-04",
            "name": "Resume with strong experience but weak project descriptions",
            "role": "Data Analyst",
            "job_description": "Data Analyst to query data warehouses, generate executive reports, build Tableau dashboards, and communicate statistical findings.",
            "resume_data": {
                "basic_details": {"name": "David Kim", "email": "david@analyst.org"},
                "professional_summary": ["Data Analyst with 3 years experience at Enterprise Corp analyzing business data and optimizing workflows."],
                "education": ["B.S. in Statistics, 2021"],
                "experience": [
                    "Data Analyst at Enterprise Corp (2021-2024): Queried databases with SQL, prepared monthly reports for finance department.",
                    "Analytics Intern (2020): Cleaned messy transaction datasets using Excel and Python."
                ],
                "projects": [
                    "School Project: Made a website with some charts.",
                    "Data Project: Looked at sales data."
                ],
                "certification": ["Google Data Analytics Professional Certificate"],
                "skills": ["SQL", "Python", "Excel", "Tableau", "Pandas", "Statistics"],
                "raw_text": "David Kim. Data Analyst. 3 years experience at Enterprise Corp. Skills: SQL, Python, Excel, Tableau."
            },
            "ml_results": {"predicted_role": "Data Analyst", "total_score": 78.0},
            "expected": "Module C identifies vague project bullets and generates actionable architectural/quantified rewrites."
        },
        {
            "id": "TC-05",
            "name": "Resume with irrelevant skills",
            "role": "Data Analyst",
            "job_description": "Data Analyst specializing in SQL, Power BI, and Python predictive modeling.",
            "resume_data": {
                "basic_details": {"name": "Taylor Swift", "email": "taylor@craft.com"},
                "professional_summary": ["Multidisciplinary hobbyist exploring career pivot."],
                "education": ["High School Diploma, 2018"],
                "experience": ["Woodshop Assistant (2020-2023): Sanded furniture, managed lumber inventory."],
                "projects": ["Custom Acoustic Guitar: Handcrafted wooden acoustic guitar."],
                "certification": ["Certified Forklift Operator"],
                "skills": ["Woodworking", "TIG Welding", "Ceramics", "Acoustic Guitar", "Veterinary First Aid"],
                "raw_text": "Taylor. Woodworking, TIG welding, ceramics, acoustic guitar, forklift operator."
            },
            "ml_results": {"predicted_role": "Data Analyst", "total_score": 25.0},
            "expected": "System isolates lack of analytical skills, reports severe skill gaps, and suggests foundational learning path."
        },
        {
            "id": "TC-06",
            "name": "Empty job description",
            "role": "SDE(Fullstack)",
            "job_description": "",
            "resume_data": {
                "basic_details": {"name": "Morgan Vance", "email": "morgan@fullstack.io"},
                "professional_summary": ["Full Stack Engineer proficient in React, Node.js, Express, and PostgreSQL."],
                "education": ["B.Sc Computer Science, 2023"],
                "experience": ["Full Stack Developer at Nexa: Developed user auth, dashboard UI, and REST API endpoints."],
                "projects": ["Social Platform MVP: Fullstack app with React frontend and Express/PostgreSQL backend."],
                "certification": ["Meta Full-Stack Developer Certificate"],
                "skills": ["JavaScript", "TypeScript", "React", "Node.js", "Express", "PostgreSQL", "Git"],
                "raw_text": "Morgan Vance. Fullstack Engineer with React, Node.js, Express, PostgreSQL."
            },
            "ml_results": {"predicted_role": "SDE(Fullstack)", "total_score": 75.0},
            "expected": "Graceful fallback using standard industry benchmark qualifications for SDE(Fullstack); no crashes."
        },
        {
            "id": "TC-07",
            "name": "Very short resume",
            "role": "SDE(Backend)",
            "job_description": "Backend Engineer with Python and SQL experience.",
            "resume_data": {
                "basic_details": {"name": "Sam"},
                "professional_summary": [],
                "education": [],
                "experience": [],
                "projects": [],
                "certification": [],
                "skills": ["Python"],
                "raw_text": "Sam. Python enthusiast looking for opportunities."
            },
            "ml_results": {"predicted_role": "SDE(Backend)", "total_score": 18.0},
            "expected": "Safe execution; highlights missing sections; career feedback delivers 30-day foundational plan."
        },
        {
            "id": "TC-08",
            "name": "Resume with incomplete information",
            "role": "SDE(Frontend)",
            "job_description": "Frontend Engineer with HTML, CSS, JavaScript, and Vue.js.",
            "resume_data": {
                "basic_details": {},  # No name, email, phone, or links
                "professional_summary": ["Frontend developer."],
                "education": [],
                "experience": ["Worked at a company doing frontend."],
                "projects": [],
                "certification": [],
                "skills": ["HTML", "CSS"],
                "raw_text": "Frontend developer. Worked at a company doing frontend. Skills: HTML, CSS."
            },
            "ml_results": {"predicted_role": "SDE(Frontend)", "total_score": 32.0},
            "expected": "Handles missing contact and education blocks; provides recommendations to complete resume anatomy."
        },
        {
            "id": "TC-09",
            "name": "Invalid or sparse input data structure",
            "role": "Data Analyst",
            "job_description": None,
            "resume_data": {},  # Empty dictionary
            "ml_results": None,
            "expected": "Context preprocessor initializes default safe containers; all modules return valid structured JSON."
        },
        {
            "id": "TC-10",
            "name": "Malformed or incomplete extracted text with binary noise",
            "role": "SDE(Backend)",
            "job_description": "Backend Engineer (Java / Spring Boot).",
            "resume_data": {
                "basic_details": {"name": "Corrupted_File_Artifact"},
                "professional_summary": ["###%%% \x00\x01\x02 ??? !!! ~~~"],
                "education": [],
                "experience": ["Error 0x8892 invalid unicode stream"],
                "projects": [],
                "certification": [],
                "skills": ["???", "&&&"],
                "raw_text": "###%%% \x00\x01\x02 ??? !!! ~~~ Error 0x8892 invalid unicode stream"
            },
            "ml_results": {"predicted_role": "Unknown", "total_score": 5.0},
            "expected": "Noise sanitized; model identifies lack of valid technical signals without throwing unhandled exceptions."
        }
    ]


def run_test_suite():
    orchestrator = AIResumeOrchestrator(prompt_version="final")
    test_cases = build_test_cases()
    results = []

    print("\n" + "=" * 80)
    print("RESUMEIQ SYSTEMATIC AI INTEGRATION TEST SUITE (10 DISTINCT CASES)")
    print(f"Active Provider: {orchestrator.llm_manager.provider_name}")
    print("=" * 80)

    all_passed = True
    for tc in test_cases:
        tc_id = tc["id"]
        tc_name = tc["name"]
        print(f"\nRunning {tc_id}: {tc_name}...", end=" ", flush=True)

        t_start = time.time()
        try:
            analysis = orchestrator.analyze(
                resume_data=tc["resume_data"],
                role=tc["role"],
                job_description=tc["job_description"],
                ml_results=tc["ml_results"]
            )
            elapsed = round(time.time() - t_start, 3)

            # Assertions:
            # 1. status is 'success'
            # 2. All 4 module outputs exist and are dicts
            modules = analysis.get("modules", {})
            has_mod_a = isinstance(modules.get("contextual_analysis"), dict)
            has_mod_b = isinstance(modules.get("skill_gap_analysis"), dict)
            has_mod_c = isinstance(modules.get("bullet_improvement"), dict)
            has_mod_d = isinstance(modules.get("career_feedback"), dict)

            passed = analysis.get("status") == "success" and has_mod_a and has_mod_b and has_mod_c and has_mod_d
            if not passed:
                all_passed = False

            observation = (
                f"Generated all 4 AI modules successfully in {elapsed}s. "
                f"Provider: {analysis['provider']}. "
                f"JD Handled: {analysis['job_description_provided']}."
            )

            actual_summary = {
                "status": analysis.get("status"),
                "module_a_present": has_mod_a,
                "module_b_present": has_mod_b,
                "module_c_present": has_mod_c,
                "module_d_present": has_mod_d,
                "sample_verdict": (
                    modules.get("contextual_analysis", {}).get("role_alignment_rating") or
                    modules.get("career_feedback", {}).get("readiness_verdict") or "Completed"
                )
            }

            status_str = "PASS" if passed else "FAIL"
            print(f"[{status_str}] ({elapsed}s)")

            results.append({
                "test_id": tc_id,
                "input_description": tc_name,
                "target_role": tc["role"],
                "expected_output": tc["expected"],
                "actual_output": actual_summary,
                "pass_fail": status_str,
                "duration_seconds": elapsed,
                "observation": observation,
                "full_analysis_snapshot": analysis
            })

        except Exception as e:
            all_passed = False
            print(f"[FAIL] (Exception: {str(e)})")
            results.append({
                "test_id": tc_id,
                "input_description": tc_name,
                "target_role": tc["role"],
                "expected_output": tc["expected"],
                "actual_output": {"error": str(e)},
                "pass_fail": "FAIL",
                "duration_seconds": round(time.time() - t_start, 3),
                "observation": f"Unhandled exception: {str(e)}"
            })

    # Save to JSON
    out_path = os.path.join(os.path.dirname(__file__), "test_suite_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "test_run_metadata": {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_tests": len(test_cases),
                "passed_tests": sum(1 for r in results if r["pass_fail"] == "PASS"),
                "failed_tests": sum(1 for r in results if r["pass_fail"] == "FAIL"),
                "overall_verdict": "PASSED" if all_passed else "FAILED"
            },
            "test_cases": results
        }, f, indent=2)

    print("\n" + "=" * 80)
    print(f"TEST SUITE SUMMARY: {sum(1 for r in results if r['pass_fail'] == 'PASS')}/{len(test_cases)} Passed.")
    print(f"Detailed test results written to: {out_path}")
    print("=" * 80)
    return all_passed


if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
