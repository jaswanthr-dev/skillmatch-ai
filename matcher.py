import re

SKILL_ALIASES = {
    "python": ["python"], "java": ["java"], "c++": ["c++"], "c": ["c"],
    "sql": ["sql", "mysql", "postgresql"], "flask": ["flask"], "django": ["django"],
    "javascript": ["javascript", "js"], "typescript": ["typescript"],
    "html": ["html", "html5"], "css": ["css", "css3"], "git": ["git"], "github": ["github"],
    "docker": ["docker"], "react": ["react"], "node.js": ["node.js"], "rest api": ["rest api"],
    "machine learning": ["machine learning", "ml"], "data structures": ["data structures"],
    "algorithms": ["algorithms"], "linux": ["linux"], "aws": ["aws"],
    "communication": ["communication"], "teamwork": ["teamwork"], "problem solving": ["problem solving"],
}

PREPARATION_TIPS = {
    "python": "Build a small Python script or CLI tool to practice core syntax and logic.",
    "java": "Write a simple Java console program to review OOP basics like classes and objects.",
    "c++": "Practice C++ fundamentals like pointers and memory management with a small project.",
    "c": "Review C basics like pointers and manual memory management with a small program.",
    "sql": "Practice writing SELECT, JOIN, and WHERE queries against a sample database.",
    "flask": "Build a tiny Flask app with one or two routes to learn the request/response cycle.",
    "django": "Follow Django's official tutorial to build a simple app and understand its structure.",
    "javascript": "Practice DOM manipulation and event handling with a small interactive webpage.",
    "typescript": "Convert a small JavaScript file to TypeScript to learn basic type annotations.",
    "html": "Build a simple multi-section webpage to practice semantic HTML tags.",
    "css": "Practice layout techniques like Flexbox or Grid on a small page design.",
    "git": "Practice basic Git commands - init, add, commit, branch, and merge - on a test repo.",
    "github": "Create a GitHub repo, push a project, and practice opening a pull request.",
    "docker": "Containerize a small app with a basic Dockerfile to learn core Docker concepts.",
    "react": "Build a small component-based UI to practice React state and props.",
    "node.js": "Build a tiny Node.js script or server to understand its event-driven model.",
    "rest api": "Build a small API endpoint and test it with a tool like Postman or curl.",
    "machine learning": "Complete a beginner ML tutorial using a small dataset to learn core concepts.",
    "data structures": "Practice implementing basic structures like stacks, queues, and linked lists.",
    "algorithms": "Solve a few beginner algorithm problems, like sorting and searching, on a practice site.",
    "linux": "Practice common Linux terminal commands for file navigation and permissions.",
    "aws": "Try AWS's free tier to deploy a small static site or basic service.",
    "communication": "Practice explaining a technical project clearly to a non-technical listener.",
    "teamwork": "Reflect on a past group project and note which collaboration habits helped most.",
    "problem solving": "Practice breaking a coding problem into smaller steps before writing any code.",
}


def normalize_text(text):
    if text is None:
        return ""
    return text.lower().strip()


def detect_skills(text, skill_aliases=SKILL_ALIASES):
    normalized = normalize_text(text)
    found_skills = set()
    for canonical_name, aliases in skill_aliases.items():
        for alias in aliases:
            escaped_alias = re.escape(alias)
            pattern = r"\b" + escaped_alias + r"\b"
            if re.search(pattern, normalized):
                found_skills.add(canonical_name)
                break
    return found_skills


def generate_preparation_checklist(missing_skills, tips=PREPARATION_TIPS):
    checklist = []
    for skill in sorted(missing_skills):
        tip = tips.get(skill, f"Learn the basics of {skill} through a short project or tutorial.")
        checklist.append(tip)
    return checklist


def match_skills(student_skills, required_skills):
    matched = student_skills & required_skills
    missing = required_skills - student_skills
    return matched, missing


def calculate_match_percentage(matched_skills, required_skills):
    total_required = len(required_skills)
    if total_required == 0:
        return None
    percentage = (len(matched_skills) / total_required) * 100
    return round(percentage, 2)


def analyze_skill_match(student_skills_text, job_description_text, skill_aliases=SKILL_ALIASES):
    student_skills = detect_skills(student_skills_text, skill_aliases)
    required_skills = detect_skills(job_description_text, skill_aliases)
    matched, missing = match_skills(student_skills, required_skills)
    percentage = calculate_match_percentage(matched, required_skills)

    if not required_skills:
        message = ("No recognizable required skills were found in the job "
                   "description. Try pasting the full description, or check "
                   "that it mentions specific tools/technologies.")
    else:
        message = None

    return {
        "student_skills": sorted(student_skills),
        "required_skills": sorted(required_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": percentage,
        "message": message,
        "checklist": generate_preparation_checklist(missing),
    }