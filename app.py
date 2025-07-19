import streamlit as st
import pdfplumber
import re

# ---------------------- CONFIGURATION ----------------------
MIN_EDUCATION_PERCENT = 50
REQUIRED_SKILLS = ["python", "java", "dbms", "os"]

# ---------------------- FUNCTIONS ----------------------

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def check_eligibility(resume_text):
    text = resume_text.lower()
    result = {"education": False, "skills": False, "missing_skills": []}

    # Check for education percentage
    found_percentages = re.findall(r'(\d{2})%', text)
    for p in found_percentages:
        if int(p) >= MIN_EDUCATION_PERCENT:
            result["education"] = True
            break

    # Check for required skills
    result["skills"] = all(skill in text for skill in REQUIRED_SKILLS)
    result["missing_skills"] = [skill for skill in REQUIRED_SKILLS if skill not in text]

    return result

# ---------------------- STREAMLIT APP ----------------------

def main():
    st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="centered")

    st.markdown(
        """
        <div style="text-align:center; padding: 20px 0;">
            <h1 style="color:#1abc9c;">📄 Resume Parser</h1>
            <p style="color:#cfcfcf;">Upload your resume and check if you're eligible based on education and skills</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("## 🎯 Eligibility Criteria")
        st.write(f"Minimum Education: **{MIN_EDUCATION_PERCENT}%**")
        st.write("Required Skills:")
        for skill in REQUIRED_SKILLS:
            st.markdown(f"- `{skill}`")

    # File type selection
    file_type = st.radio("Select Resume File Type:", ["PDF", "Plain Text (.txt)"])

    if file_type == "PDF":
        uploaded_files = st.file_uploader("📤 Upload PDF Resume(s)", type=["pdf"], accept_multiple_files=True)
    else:
        uploaded_files = st.file_uploader("📤 Upload Plain Text Resume(s)", type=["txt"], accept_multiple_files=True)

    if uploaded_files:
        for idx, uploaded_file in enumerate(uploaded_files, start=1):
            st.markdown(f"---\n## 📁 Resume {idx}: `{uploaded_file.name}`")

            # Extract text
            if file_type == "PDF":
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8")

            st.markdown("### 📃 Extracted Resume Text")
            st.text_area(f"Resume Content ({uploaded_file.name})", resume_text, height=300, key=uploaded_file.name)

            # Eligibility check
            st.markdown("### ✅ Eligibility Check")
            eligibility = check_eligibility(resume_text)

            if eligibility["education"] and eligibility["skills"]:
                st.success("🎉 You are eligible for the job!")
            else:
                st.error("❌ You are not eligible.")

            # Show results
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📘 Education Criteria Met:**")
                st.markdown("✅ Yes" if eligibility["education"] else "❌ No")
            with col2:
                st.markdown("**💼 Skills Criteria Met:**")
                st.markdown("✅ Yes" if eligibility["skills"] else "❌ No")

            if not eligibility["skills"] and eligibility["missing_skills"]:
                st.warning("⚠️ Missing Skills: " + ", ".join(eligibility["missing_skills"]))

# Run the app
if __name__ == "__main__":
    main()
