# 📄 AI Resume Screener

A **Streamlit web app** that automatically ranks resumes against a job description using **TF-IDF vectorization** and **cosine similarity**. Upload multiple PDF/DOCX resumes, paste the job description, and get a ranked list of top candidates in seconds — with color-coded match scores and one-click CSV export.

---

## 🎯 Problem Statement

Recruiters receive **hundreds of resumes per job opening**. Manually screening them is slow, inconsistent, and biased. This tool automates the first-pass screening by scoring each resume against the job description using NLP — so recruiters can focus on the top 10 instead of reading all 300.

---

## ✨ Features

- 📤 **Multi-file upload** — PDF and DOCX resumes at once
- 🎯 **Job description input** — paste any JD and get instant matching
- 🧠 **TF-IDF + Cosine Similarity** scoring engine
- 🎨 **Color-coded results** — Green (≥80%), Yellow (50–79%), Red (<50%)
- 🏆 **Top Match highlight** card for the best candidate
- 📥 **CSV download** — export ranked results for the hiring team
- ⚡ **Runs in ~10 seconds** for 5+ resumes

---

## 🖥️ App Preview
┌─────────────────────────────────────────────────────┐
│ 📄 AI Resume Screener │
│ Upload Resumes → Paste JD → Get Top Candidates │
├──────────────────────┬──────────────────────────────┤
│ 📤 Upload Resumes │ 🎯 Job Description │
│ [Choose files] │ [Paste JD here...] │
│ │ │
│ [🚀 Find Top Candidates] │
│ │
│ Rank │ Resume │ Match Score (%) │
│ ─────┼───────────────────┼──────────────────── │
│ 1 │ Amit_DS.docx │ 78.4 (Yellow) │
│ 2 │ Sneha_ML.docx │ 72.1 (Yellow) │
│ 3 │ Vikram_SE.docx │ 12.3 (Red) │
│ │
│ 🏆 Top Match: Amit_DS.docx — 78.4% │
│ [📥 Download Results as CSV] │
└─────────────────────────────────────────────────────┘

text

---

## 🧠 How It Works

### Pipeline
Upload Files → Extract Text → Clean → Preprocess → TF-IDF Vectorize → Cosine Similarity → Rank → Display

text

### 1. Text Extraction (`resume_extractor.py`)
- **PDF:** `pdfplumber` extracts text page-by-page
- **DOCX:** `python-docx` extracts paragraph text
- **Cleaning:** removes extra whitespace, non-ASCII noise, and repeated newlines

### 2. Preprocessing (`resume_matcher.py`)
- Lowercase, strip special characters, collapse whitespace
- English stop-word removal via scikit-learn's `TfidfVectorizer`

### 3. Matching Engine (`resume_matcher.py`)
- **TF-IDF** converts the job description + all resumes into a shared vector space
- **`max_features=500`** keeps the strongest 500 terms (avoids noise from rare words)
- **Cosine similarity** measures the angle between the JD vector and each resume vector — score from 0 to 100%
- Results sorted descending, so the best match is always on top

### 4. UI (`app.py`)
- Built with **Streamlit** — columns, sidebar, spinners, color-coded dataframe
- Uploaded files saved to a temp directory, processed, then cleaned up with `shutil.rmtree`

---

## 📊 Example Result

**Job Description:** *"Data Scientist with Python, ML, Pandas, Scikit-learn, AWS, and Deep Learning"*

| Rank | Resume | Score |

| 1 | Amit_Data_Scientist.docx | 78.4% |
| 2 | Sneha_MLEngineer.docx | 72.1% |
| 3 | Rahul_Data_Analyst.docx | 31.5% |
| 4 | Priya_Python_Developer.docx | 18.2% |
| 5 | Vikram_Software_Engineer.docx | 12.3% |

The DS profile ranks first because it shares the most TF-IDF terms with the JD ("data scientist", "machine learning", "python", "scikit-learn"). The full-stack engineer scores lowest — expected, since the JD has zero Java/Angular terms.

---

## 🛠️ Tech Stack

| Layer | Technology |

| **UI** | Streamlit |
| **NLP / Matching** | scikit-learn (`TfidfVectorizer`, `cosine_similarity`) |
| **PDF parsing** | pdfplumber |
| **DOCX parsing** | python-docx |
| **Data handling** | Pandas, NumPy |
| **Language** | Python 3.10+ |

---

## 📦 Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB/ai-resume-screener.git
cd ai-resume-screener
Step 2 — Create a virtual environment (recommended)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
Step 3 — Install dependencies
bash
pip install -r requirements.txt
If you don't have requirements.txt, install manually:

bash
pip install streamlit pandas scikit-learn pdfplumber python-docx
Step 4 — Launch the app
bash
streamlit run app.py
The app opens at http://localhost:8501 in your browser.

▶️ How to Use
Open the app in your browser

Upload resumes (PDF or DOCX — multiple files allowed)

Paste the job description in the text box on the right

Click 🚀 Find Top Candidates

View the ranked results table with color-coded scores

Click 📥 Download Results as CSV to save for your team

📁 Folder Structure
text
ai-resume-screener/
├── app.py                              # Streamlit UI
├── resume_extractor.py                 # PDF/DOCX text extraction + cleaning
├── resume_matcher.py                   # TF-IDF + cosine similarity engine
├── requirements.txt                    # Python dependencies
├── sample_resume.docx                  # Demo resume for testing
├── dummy_Amit_Data_Scientist.docx      # Test resume — Data Scientist
├── dummy_Priya_Python_Developer.docx   # Test resume — Python Developer
├── dummy_Rahul_Data_Analyst.docx       # Test resume — Data Analyst
├── dummy_Sneha_MLEngineer.docx         # Test resume — ML Engineer
├── dummy_Vikram_Software_Engineer.docx # Test resume — Software Engineer
└── README.md
🚀 What I Would Do Next
Semantic embeddings — replace TF-IDF with sentence-transformers (all-MiniLM-L6-v2) to capture meaning, not just keyword overlap

Skill extraction — parse structured skills using spaCy and score per-category (e.g., 90% on Python, 40% on AWS)

Experience filter — auto-extract years of experience with regex and filter by JD requirement

Bias mitigation — strip names, gender, and location before scoring to reduce unconscious bias

Deploy — host on Streamlit Community Cloud (free) so recruiters can use it without installing anything

Multi-tenant SaaS — add login + per-company storage for a real product version

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

📄 License
This project is open-source and available under the MIT License.
