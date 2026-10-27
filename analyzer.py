import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Get the directory containing this Python file.
BASE_DIRECTORY = Path(__file__).resolve().parent

# Build the complete path to the skills dataset.
SKILLS_FILE = BASE_DIRECTORY / "data" / "skills.json"


def load_skills():
    """
    Load categorized skills from skills.json.

    Returns:
        dict: Skill categories and their associated skills.
    """

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_text(text):
    """
    Clean and standardize resume or job-description text.

    Args:
        text (str): Original text.

    Returns:
        str: Cleaned lowercase text.
    """

    text = text.lower()

    # Keep letters, numbers and symbols commonly found in skills.
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    # Replace consecutive spaces with one space.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_skill(text, skill):
    """
    Check whether a complete skill exists in text.

    This prevents 'java' from matching 'javascript'.

    Args:
        text (str): Cleaned text.
        skill (str): Skill being searched.

    Returns:
        bool: True when the skill is found.
    """

    escaped_skill = re.escape(skill)

    pattern = (
        rf"(?<![a-z0-9])"
        rf"{escaped_skill}"
        rf"(?![a-z0-9])"
    )

    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_skills(text):
    """
    Extract recognized skills and preserve their categories.

    Args:
        text (str): Resume or job-description text.

    Returns:
        dict: Found skills grouped by category.
    """

    cleaned_text = clean_text(text)
    categorized_skills = load_skills()

    found_skills = {}

    for category, skills in categorized_skills.items():
        category_matches = []

        for skill in skills:
            if contains_skill(cleaned_text, skill):
                category_matches.append(skill)

        if category_matches:
            found_skills[category] = sorted(category_matches)

    return found_skills


def flatten_skills(categorized_skills):
    """
    Convert categorized skills into one set.

    Args:
        categorized_skills (dict): Skills grouped by category.

    Returns:
        set: Unique skill names.
    """

    return {
        skill
        for skills in categorized_skills.values()
        for skill in skills
    }


def calculate_text_similarity(
    resume_text,
    job_description
):
    """
    Calculate TF-IDF cosine similarity.

    Args:
        resume_text (str): Candidate's resume content.
        job_description (str): Job requirements.

    Returns:
        float: Similarity percentage from 0 to 100.
    """

    cleaned_resume = clean_text(resume_text)
    cleaned_job = clean_text(job_description)

    if not cleaned_resume or not cleaned_job:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        [cleaned_resume, cleaned_job]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def calculate_skill_score(
    matched_skills,
    required_skills
):
    """
    Calculate required-skills coverage.

    Returns:
        float: Skill coverage percentage.
    """

    if not required_skills:
        return 0.0

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(score, 2)


def generate_recommendation(
    skill_score,
    missing_skills
):
    """
    Generate a basic career recommendation.
    """

    if not missing_skills:
        return (
            "The resume contains all recognized skills from "
            "the job description. Support these skills with "
            "projects and measurable achievements."
        )

    top_missing_skills = ", ".join(missing_skills[:5])

    if skill_score >= 70:
        return (
            "The resume is a strong skills match. Consider "
            "learning or demonstrating these remaining skills: "
            f"{top_missing_skills}."
        )

    if skill_score >= 40:
        return (
            "The resume is a moderate skills match. Prioritize "
            f"these missing skills: {top_missing_skills}."
        )

    return (
        "The current skills match is limited. Review the role "
        "carefully and begin developing these skills: "
        f"{top_missing_skills}."
    )


def analyze_resume(
    resume_text,
    job_description
):
    """
    Perform the complete resume analysis.

    Returns:
        dict: Scores, skills and recommendation.
    """

    resume_categories = extract_skills(resume_text)
    job_categories = extract_skills(job_description)

    resume_skills = flatten_skills(resume_categories)
    required_skills = flatten_skills(job_categories)

    matched_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills.difference(resume_skills)
    )

    additional_skills = sorted(
        resume_skills.difference(required_skills)
    )

    skill_score = calculate_skill_score(
        matched_skills,
        required_skills
    )

    text_similarity = calculate_text_similarity(
        resume_text,
        job_description
    )

    # Skills have 70% weight, textual similarity has 30%.
    overall_score = round(
        (skill_score * 0.70)
        + (text_similarity * 0.30),
        2
    )

    recommendation = generate_recommendation(
        skill_score,
        missing_skills
    )

    return {
        "overall_score": overall_score,
        "skill_score": skill_score,
        "text_similarity": text_similarity,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "required_skills": sorted(required_skills),
        "resume_skill_categories": resume_categories,
        "job_skill_categories": job_categories,
        "recommendation": recommendation
    }