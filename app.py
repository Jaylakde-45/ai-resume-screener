import streamlit as st
import pandas as pd
import os
import tempfile
from resume_extractor import extract_resume_text, clean_resume_text
from resume_matcher import match_resumes, preprocess_text

# =============================================
# 📱 STREAMLIT UI - RESUME SCREENER (Day 3)
# =============================================

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <div style="background-color: #1a5f1a; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: white;">📄 AI Resume Screener</h1>
        <p style="color: #DCF8C6;">Upload Resumes, Enter Job Description, Get Top Candidates in 10 Seconds</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# --- Sidebar Instructions ---
with st.sidebar:
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Upload Resumes** (PDF or DOCX)
    2. **Paste the Job Description**
    3. **Click "Find Top Candidates"**
    4. **Download the results as CSV**
    """)
    st.markdown("---")
    st.caption("💡 **₹5,000/month** | 7 Days Free Trial")

# --- Main Area ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Choose PDF or DOCX files",
        type=['pdf', 'docx'],
        accept_multiple_files=True,
        key="resume_uploader"
    )

with col2:
    st.markdown("### 🎯 Job Description")
    job_description = st.text_area(
        "Paste the job requirements here",
        height=200,
        placeholder="Example: Looking for a Data Scientist with 3+ years experience in Python, Machine Learning, and deploying models in production."
    )

# --- Process Button ---
if st.button("🚀 Find Top Candidates", use_container_width=True, type="primary"):
    
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
    elif not job_description.strip():
        st.warning("⚠️ Please enter a job description.")
    else:
        with st.spinner("🧠 Extracting text and matching resumes..."):
            
            # 1. Save uploaded files temporarily
            temp_dir = tempfile.mkdtemp()
            resume_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                resume_paths.append(file_path)
            
            # 2. Run the matcher
            results_df = match_resumes(job_description, resume_paths)
            
            # 3. Display Results
            if not results_df.empty:
                st.success(f"✅ Found {len(results_df)} resumes! Top matches below.")
                
                # Add Rank column
                results_df.index = results_df.index + 1
                results_df.index.name = 'Rank'
                
                 # Format the Match Score column with color
                def color_score(val):
                    if val >= 80:
                        return 'background-color: #d4edda; color: #155724;'  # Green
                    elif val >= 50:
                        return 'background-color: #fff3cd; color: #856404;'  # Yellow
                    else:
                        return 'background-color: #f8d7da; color: #721c24;'  # Red
                
                # ✅ FIXED: Changed applymap to map (Pandas 3.0+)
                styled_df = results_df.style.map(color_score, subset=['Match Score (%)'])
                
                               # Show the table
                st.dataframe(styled_df, use_container_width=True)
                
                # Highlight Top Match
                top_candidate = results_df.iloc[0]   # <--- ADD THIS LINE
                st.markdown(f"""
                <div style="background-color: #d4edda; padding: 15px; border-radius: 10px; border: 2px solid #28a745;">
                    <h3 style="color: #155724;">🏆 Top Match: {top_candidate['Resume']}</h3>
                    <p style="font-size: 20px; color: #155724; font-weight: bold;">Match Score: {top_candidate['Match Score (%)']}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download button
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="resume_matches.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Clean up temp files
                import shutil
                shutil.rmtree(temp_dir)
                
            else:
                st.error("❌ No resumes were successfully read. Please check the file formats.")

# --- Footer ---
st.markdown("---")
st.caption("💡 **Tip:** For best results, ensure the job description is detailed and the resumes are in text-based PDF or DOCX format.")