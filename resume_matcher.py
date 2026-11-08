import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_extractor import extract_resume_text, clean_resume_text

# =============================================
# 🧠 RESUME MATCHER (Day 2)
# =============================================

def preprocess_text(text):
    """
    Clean and preprocess text for TF-IDF.
    - Lowercase
    - Remove special characters
    - Remove extra spaces
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def match_resumes(job_description, resume_files):
    """
    Takes a job description and a list of resume file paths.
    Returns a sorted DataFrame with match scores.
    """
    # Step 1: Extract and clean text from all resumes
    resume_texts = []
    valid_files = []
    
    for file_path in resume_files:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        raw_text = extract_resume_text(file_path)
        clean_text = clean_resume_text(raw_text)
        if clean_text:
            resume_texts.append(clean_text)
            valid_files.append(file_path)
        else:
            print(f"⚠️ No text extracted from: {file_path}")
    
    if not resume_texts:
        print("❌ No valid resumes found.")
        return pd.DataFrame()
    
    # Step 2: Preprocess all texts (including JD)
    processed_resumes = [preprocess_text(text) for text in resume_texts]
    processed_jd = preprocess_text(job_description)
    
    # Step 3: Combine all texts for TF-IDF (JD + Resumes)
    all_texts = [processed_jd] + processed_resumes
    
    # Step 4: Create TF-IDF Vectors
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Step 5: Calculate Cosine Similarity (JD vs each resume)
    jd_vector = tfidf_matrix[0]  # First row is JD
    resume_vectors = tfidf_matrix[1:]  # Remaining rows are resumes
    similarity_scores = cosine_similarity(jd_vector, resume_vectors).flatten()
    
    # Step 6: Create Results DataFrame
    results = []
    for idx, file_path in enumerate(valid_files):
        results.append({
            'Resume': os.path.basename(file_path),
            'Match Score (%)': round(similarity_scores[idx] * 100, 2),
            'File Path': file_path
        })
    
    # Step 7: Sort by score (highest first)
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('Match Score (%)', ascending=False)
    results_df = results_df.reset_index(drop=True)
    
    return results_df

# =============================================
# 🚀 TESTING (Day 2)
# =============================================

if __name__ == "__main__":
    print("="*60)
    print("🧠 RESUME MATCHER - DAY 2 TEST")
    print("="*60)
    
    # 1. Create multiple dummy resumes for testing
    from docx import Document
    
    print("\n📄 Generating 5 dummy resumes for testing...")
    
    dummy_resumes = [
        {
            "name": "Amit_Data_Scientist",
            "content": """Summary: Data Scientist with 5 years experience in Python, Machine Learning, and Deep Learning. 
            Skills: Python, TensorFlow, PyTorch, SQL, Pandas, Scikit-learn.
            Experience: Built predictive models for e-commerce. Deployed ML models on AWS."""
        },
        {
            "name": "Priya_Python_Developer",
            "content": """Summary: Python Developer with 3 years experience in web development and automation.
            Skills: Python, Django, Flask, REST APIs, Git, Docker.
            Experience: Developed backend services for fintech startups."""
        },
        {
            "name": "Rahul_Data_Analyst",
            "content": """Summary: Data Analyst with 4 years experience in Excel, SQL, and Power BI.
            Skills: SQL, Excel, Tableau, Power BI, Data Visualization.
            Experience: Created dashboards for sales teams. Analyzed customer churn."""
        },
        {
            "name": "Sneha_MLEngineer",
            "content": """Summary: ML Engineer with 6 years experience in deploying machine learning models.
            Skills: Python, TensorFlow, Docker, Kubernetes, MLOps, AWS.
            Experience: Deployed real-time recommendation systems. Led ML teams."""
        },
        {
            "name": "Vikram_Software_Engineer",
            "content": """Summary: Full Stack Developer with 7 years experience in Java, Spring Boot, and Angular.
            Skills: Java, Spring Boot, Angular, MySQL, Microservices.
            Experience: Built scalable enterprise applications."""
        }
    ]
    
    resume_files = []
    for i, dummy in enumerate(dummy_resumes):
        filename = f"dummy_{dummy['name']}.docx"
        doc = Document()
        doc.add_paragraph(dummy['content'])
        doc.save(filename)
        resume_files.append(filename)
        print(f"  ✅ Created: {filename}")
    
    # 2. Define a Job Description (Data Scientist)
    job_description = """
    We are looking for a Data Scientist with strong experience in Python, Machine Learning, and deploying models in production. 
    Must have hands-on experience with Pandas, Scikit-learn, and cloud platforms like AWS. 
    Knowledge of Deep Learning (TensorFlow/PyTorch) is a plus.
    """
    
    # 3. Run the matcher
    print("\n" + "="*60)
    print("🔍 MATCHING RESUMES AGAINST JOB DESCRIPTION")
    print("="*60)
    print(f"\n📝 JD: {job_description.strip()[:100]}...\n")
    
    results = match_resumes(job_description, resume_files)
    
    if not results.empty:
        print("✅ MATCH RESULTS (Top 5):")
        print("="*60)
        print(results.to_string(index=False))
        print("\n✅ SUCCESS: Matching engine is working!")
    else:
        print("❌ No results. Please check the resumes.")
    
    print("\n💡 Tomorrow (Day 3): We will build the Streamlit UI for this engine.")