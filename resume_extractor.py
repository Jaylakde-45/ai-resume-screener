import pdfplumber
import docx
import os
import re

# =============================================
# 📄 RESUME TEXT EXTRACTOR (Day 1)
# 100% Reliable - No OCR required
# =============================================

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using pdfplumber.
    Works on text-based PDFs (not scanned images).
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """
    Extracts text from a Word (DOCX) file using python-docx.
    """
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading DOCX {file_path}: {e}")
        return ""

def extract_resume_text(file_path):
    """
    Detects the file type and extracts text accordingly.
    Supports: .pdf, .docx
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return ""

    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        print(f"📄 Extracting text from PDF: {file_path}")
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        print(f"📄 Extracting text from DOCX: {file_path}")
        return extract_text_from_docx(file_path)
    else:
        print(f"❌ Unsupported file type: {file_extension}")
        return ""

def clean_resume_text(raw_text):
    """
    Cleans the extracted text by removing excessive spaces, special characters, and common noise.
    """
    if not raw_text:
        return ""
    
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', raw_text)
    # Remove excessive spaces
    text = re.sub(r' +', ' ', text)
    # Remove weird Unicode characters (keep basic ones)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    return text.strip()

# =============================================
# 🚀 TESTING (Day 1)
# =============================================

if __name__ == "__main__":
    # 1. Create a sample resume for testing (if you don't have one)
    sample_path = "sample_resume.docx"
    
    if not os.path.exists(sample_path):
        print("⚠️ No sample resume found. Creating a dummy sample.docx for testing...")
        from docx import Document
        doc = Document()
        doc.add_heading('Resume - John Doe', 0)
        doc.add_paragraph('Email: john.doe@email.com')
        doc.add_paragraph('Phone: +91 98765 43210')
        doc.add_paragraph('Summary: Data Scientist with 3 years of experience in Python, Machine Learning, and Analytics.')
        doc.add_paragraph('Skills: Python, SQL, Pandas, Scikit-learn, Streamlit')
        doc.add_paragraph('Experience:')
        doc.add_paragraph('  - Data Analyst at XYZ Corp (2021-2024)')
        doc.add_paragraph('  - Built dashboards and predictive models.')
        doc.save(sample_path)
        print(f"✅ Created sample resume: {sample_path}")

    # 2. Extract text from the sample file
    raw_text = extract_resume_text(sample_path)
    clean_text = clean_resume_text(raw_text)
    
    print("\n" + "="*60)
    print("🧾 EXTRACTED RESUME TEXT")
    print("="*60)
    if clean_text:
        print(clean_text)
        print("\n✅ SUCCESS: Text extraction is working!")
    else:
        print("❌ No text extracted. Please check the file format.")