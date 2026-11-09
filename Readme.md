# AI Career Companion

AI Career Companion is a full-stack NLP-based web application that compares a candidate's resume with a job description. It calculates compatibility scores, identifies matched and missing skills, highlights additional resume skills, and generates a practical career recommendation.

## Features

- Compare resume text with a job description
- Extract technical and soft skills from both inputs
- Identify matched skills
- Detect missing job requirements
- Highlight additional skills found in the resume
- Calculate skill coverage percentage
- Calculate TF-IDF text similarity
- Generate a weighted overall compatibility score
- Produce an automated career recommendation
- Responsive web interface
- REST API with interactive Swagger documentation

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic

### NLP and Machine Learning

- Scikit-learn
- TF-IDF vectorization
- Cosine similarity
- Rule-based skill extraction

### Frontend

- HTML
- CSS
- JavaScript

### Data

- JSON-based categorized skills dataset

## How It Works

1. The user enters resume text and a job description.
2. JavaScript sends both inputs to the FastAPI backend.
3. Python cleans and normalizes the supplied text.
4. The analyzer extracts recognized skills using `skills.json`.
5. Scikit-learn converts the documents into TF-IDF vectors.
6. Cosine similarity measures textual relevance.
7. The application calculates matched, missing, additional, and required skills.
8. FastAPI returns the analysis as JSON.
9. JavaScript displays the results as a career compatibility report.

## Scoring Formula

The application gives more importance to required skill coverage than general textual similarity:

```text
Overall Score = (Skill Coverage x 0.70) + (Text Similarity x 0.30)
```

### Example

```text
Skill Coverage: 60.00%
Text Similarity: 17.27%

Overall Score = (60.00 x 0.70) + (17.27 x 0.30)
Overall Score = 47.18%
```

## Project Structure

```text
Rising-Up/
|-- data/
|   `-- skills.json
|-- frontend/
|   |-- mainpage.html
|   |-- scripts.js
|   `-- styles.css
|-- analyzer.py
|-- main.py
|-- test_analyzer.py
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Faizan-15/Rising-Up.git
cd Rising-Up
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

#### Linux or macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

### 6. Open the application

Open the following address in a browser:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "application": "AI Career Companion",
  "status": "healthy"
}
```

### Analyze Resume

```http
POST /api/analyze
```

Example request body:

```json
{
  "resume_text": "Computer Science student experienced in Python, JavaScript, SQL, Git, Pandas and teamwork.",
  "job_description": "We need a Python developer with JavaScript, SQL, Git, Docker, Linux and communication skills."
}
```

Example response structure:

```json
{
  "overall_score": 47.18,
  "skill_score": 60.0,
  "text_similarity": 17.27,
  "matched_skills": [
    "git",
    "javascript",
    "python",
    "sql"
  ],
  "missing_skills": [
    "communication",
    "docker",
    "linux"
  ],
  "additional_skills": [
    "pandas",
    "teamwork"
  ],
  "required_skills": [
    "communication",
    "docker",
    "git",
    "javascript",
    "linux",
    "python",
    "sql"
  ],
  "recommendation": "The resume is a moderate skills match. Prioritize the missing skills."
}
```

The exact scores depend on the supplied resume and job description.

## Running the Python Analyzer Directly

The analysis engine can be tested without opening the web interface:

```bash
python test_analyzer.py
```

This displays:

- Overall compatibility score
- Skill coverage score
- Text similarity score
- Matched skills
- Missing skills
- Additional resume skills
- Career recommendation

## Main Files

### `analyzer.py`

Contains the core NLP and analysis logic:

- Text cleaning
- Skill extraction
- Skill comparison
- TF-IDF vectorization
- Cosine similarity
- Score calculation
- Recommendation generation

### `main.py`

Contains the FastAPI application:

- Serves the custom frontend page
- Serves CSS and JavaScript static files
- Provides the health-check endpoint
- Provides the resume-analysis endpoint
- Validates API input using Pydantic

### `data/skills.json`

Stores categorized skills, including:

- Programming languages
- Web development technologies
- Databases
- Artificial intelligence and data skills
- Development tools and cloud platforms
- Soft skills

### `frontend/mainpage.html`

Defines the user interface for resume and job-description input and the compatibility report.

### `frontend/styles.css`

Provides the responsive dark-themed interface, result cards, score bars, skill badges, and mobile layout.

### `frontend/scripts.js`

Connects the frontend to FastAPI using `fetch()`, validates user input, displays loading and error states, and renders the returned analysis.

## Current Limitations

- Resume text must currently be pasted manually.
- Skill detection depends on the entries available in `skills.json`.
- TF-IDF measures word-level textual similarity and may not fully understand semantic meaning.
- Skill experience level and years of experience are not yet evaluated.
- Scanned or image-based resumes are not currently supported.
- The result is an automated estimate and does not represent a hiring decision.

## Future Improvements

- PDF resume upload and text extraction
- DOCX resume support
- Skill aliases and normalization
- Semantic matching with sentence-transformer embeddings
- Education and experience extraction
- Weighted job requirements
- Resume improvement suggestions
- Downloadable PDF compatibility report
- Automated backend tests with Pytest
- Cloud deployment

## Privacy

The current application processes the supplied text for analysis. Avoid entering confidential personal data when using an untrusted or publicly deployed instance. A production deployment should include appropriate privacy controls, input-size restrictions, secure logging, and a clear data-retention policy.

## Disclaimer

AI Career Companion is an educational project. Compatibility scores and recommendations are automated estimates based on recognized skills and textual similarity. The results should not be treated as professional recruitment advice or a final hiring decision.

## Author

**Muhammad Faizan Ashraf**

- GitHub: [Faizan-15](https://github.com/Faizan-15)
- Repository: [Rising-Up](https://github.com/Faizan-15/Rising-Up.git)

## License

This project is currently provided for educational and portfolio purposes. Add a `LICENSE` file before declaring a specific open-source license.
