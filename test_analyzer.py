from analyzer import analyze_resume


resume = """
Muhammad is a Computer Science student with experience
in Python, JavaScript, HTML, CSS, Oracle SQL, Git and GitHub.

The candidate has developed web applications and completed
data analysis projects using Pandas and NumPy.

The candidate also possesses teamwork and problem-solving
skills.
"""


job_description = """
We are looking for a junior Python developer.

The candidate should know Python, JavaScript, SQL, Git,
Docker and Linux. Strong problem solving, teamwork and
communication skills are required.

Experience with FastAPI is preferred.
"""


result = analyze_resume(
    resume,
    job_description
)


print("\nAI CAREER COMPANION")
print("=" * 50)

print(
    f"Overall Score: "
    f"{result['overall_score']}%"
)

print(
    f"Skill Coverage: "
    f"{result['skill_score']}%"
)

print(
    f"Text Similarity: "
    f"{result['text_similarity']}%"
)

print("\nRequired Skills:")

for skill in result["required_skills"]:
    print(f"  - {skill}")

print("\nMatched Skills:")

for skill in result["matched_skills"]:
    print(f"  + {skill}")

print("\nMissing Skills:")

for skill in result["missing_skills"]:
    print(f"  - {skill}")

print("\nAdditional Resume Skills:")

for skill in result["additional_skills"]:
    print(f"  * {skill}")

print("\nRecommendation:")
print(result["recommendation"])