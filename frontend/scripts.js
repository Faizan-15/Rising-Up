const resumeInput = document.getElementById("resumeText");
const jobInput = document.getElementById("jobDescription");

const resumeCount = document.getElementById("resumeCount");
const jobCount = document.getElementById("jobCount");

const analyzeButton =
    document.getElementById("analyzeButton");

const errorMessage =
    document.getElementById("errorMessage");

const loadingSection =
    document.getElementById("loadingSection");

const resultsSection =
    document.getElementById("resultsSection");


resumeInput.addEventListener("input", () => {
    updateCharacterCount(resumeInput, resumeCount);
});

jobInput.addEventListener("input", () => {
    updateCharacterCount(jobInput, jobCount);
});

analyzeButton.addEventListener("click", analyzeResume);


function updateCharacterCount(input, output) {
    const count = input.value.length;

    output.textContent =
        `${count} character${count === 1 ? "" : "s"}`;
}


async function analyzeResume() {
    const resumeText = resumeInput.value.trim();
    const jobDescription = jobInput.value.trim();

    clearError();

    if (!resumeText || !jobDescription) {
        showError(
            "Please enter both the resume text " +
            "and job description."
        );

        return;
    }

    if (resumeText.length < 30) {
        showError(
            "The resume text must contain at least 30 characters."
        );

        return;
    }

    if (jobDescription.length < 30) {
        showError(
            "The job description must contain at least 30 characters."
        );

        return;
    }

    setLoadingState(true);

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                resume_text: resumeText,
                job_description: jobDescription
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                readApiError(data)
            );
        }

        displayResults(data);

    } catch (error) {
        showError(
            error.message ||
            "The analysis could not be completed."
        );

    } finally {
        setLoadingState(false);
    }
}


function readApiError(data) {
    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (Array.isArray(data.detail)) {
        return data.detail
            .map((item) => item.msg)
            .join(" ");
    }

    return "The analysis request failed.";
}


function displayResults(data) {
    resultsSection.classList.remove("hidden");

    setScore(
        "overallScore",
        "overallProgress",
        data.overall_score
    );

    setScore(
        "skillScore",
        "skillProgress",
        data.skill_score
    );

    setScore(
        "textSimilarity",
        "similarityProgress",
        data.text_similarity
    );

    renderSkills(
        "matchedSkills",
        data.matched_skills,
        "matched",
        "No required skills matched."
    );

    renderSkills(
        "missingSkills",
        data.missing_skills,
        "missing",
        "No recognized required skills are missing."
    );

    renderSkills(
        "additionalSkills",
        data.additional_skills,
        "additional",
        "No additional recognized skills were found."
    );

    renderSkills(
        "requiredSkills",
        data.required_skills,
        "",
        "No supported job requirements were recognized."
    );

    document.getElementById("matchedCount").textContent =
        data.matched_skills.length;

    document.getElementById("missingCount").textContent =
        data.missing_skills.length;

    document.getElementById("additionalCount").textContent =
        data.additional_skills.length;

    document.getElementById("requiredCount").textContent =
        data.required_skills.length;

    document.getElementById("recommendation").textContent =
        data.recommendation;

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function setScore(
    valueElementId,
    progressElementId,
    score
) {
    const numericScore = Number(score);

    const safeScore = Number.isFinite(numericScore)
        ? Math.min(Math.max(numericScore, 0), 100)
        : 0;

    document.getElementById(
        valueElementId
    ).textContent = `${safeScore.toFixed(2)}%`;

    document.getElementById(
        progressElementId
    ).style.width = `${safeScore}%`;
}


function renderSkills(
    containerId,
    skills,
    className,
    emptyMessage
) {
    const container =
        document.getElementById(containerId);

    container.replaceChildren();

    if (!Array.isArray(skills) || skills.length === 0) {
        const message = document.createElement("p");

        message.className = "empty-message";
        message.textContent = emptyMessage;

        container.appendChild(message);
        return;
    }

    skills.forEach((skill) => {
        const element = document.createElement("span");

        element.className =
            `skill ${className}`.trim();

        element.textContent = formatSkillName(skill);

        container.appendChild(element);
    });
}


function formatSkillName(skill) {
    return skill
        .split(" ")
        .map((word) => {
            const specialNames = {
                "api": "API",
                "aws": "AWS",
                "css": "CSS",
                "git": "Git",
                "github": "GitHub",
                "html": "HTML",
                "javascript": "JavaScript",
                "linux": "Linux",
                "numpy": "NumPy",
                "pandas": "Pandas",
                "python": "Python",
                "sql": "SQL"
            };

            return (
                specialNames[word] ||
                word.charAt(0).toUpperCase() + word.slice(1)
            );
        })
        .join(" ");
}


function setLoadingState(isLoading) {
    analyzeButton.disabled = isLoading;

    analyzeButton.textContent = isLoading
        ? "Analyzing..."
        : "Analyze Resume";

    loadingSection.classList.toggle(
        "hidden",
        !isLoading
    );
}


function showError(message) {
    errorMessage.textContent = message;
}


function clearError() {
    errorMessage.textContent = "";
}