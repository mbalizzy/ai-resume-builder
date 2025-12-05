import streamlit as st
from jinja2 import Environment, FileSystemLoader
import os
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Remove WeasyPrint for now (requires Pango/Cairo on Linux)
# from weasyprint import HTML  # ❌

# ✅ Remove Windows-specific wkhtmltopdf path and configuration
# import pdfkit  # we'll import inside the PDF block safely

# Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

# DOCX export helper
def export_docx(name, email, phone, summary, skills, experience, education, output_path):
    doc = Document()
    doc.add_heading(name or "Unnamed", 0)
    if email:
        doc.add_paragraph(f"Email: {email}")
    if phone:
        doc.add_paragraph(f"Phone: {phone}")

    if summary:
        doc.add_heading("Professional Summary", level=1)
        doc.add_paragraph(summary)

    if skills:
        doc.add_heading("Key Skills", level=1)
        for skill in skills:
            doc.add_paragraph(skill, style="List Bullet")

    if experience:
        doc.add_heading("Work Experience", level=1)
        doc.add_paragraph(experience)

    if education:
        doc.add_heading("Education", level=1)
        doc.add_paragraph(education)

    doc.save(output_path)

# Match score
def match_score(resume_text, job_text):
    vectorizer = TfidfVectorizer().fit([resume_text, job_text])
    vectors = vectorizer.transform([resume_text, job_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

# Page
st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder")

# Form
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    summary = st.text_area("Professional Summary")
    skills = st.text_area("Skills (comma-separated)")
    experience = st.text_area("Work Experience")
    education = st.text_area("Education")
    job_description = st.text_area("Paste Job Description (optional)")
    template_choice = st.selectbox(
        "Choose a Template",
        ["resume_template1.html", "resume_template2.html", "resume_template3.html"]
    )
    submitted = st.form_submit_button("Generate Resume")  # ✅ ensures submit exists

if submitted:
    # Prepare data
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    template = env.get_template(template_choice)
    html = template.render(
        name=name,
        email=email,
        phone=phone,
        summary=summary,
        skills=skills_list,
        experience=experience,
        education=education
    )

    # Preview
    st.markdown("### 💡 Resume Preview")
    st.components.v1.html(html, height=800, scrolling=True)

    # Downloads
    st.markdown("### 📥 Download Options")

    # HTML
    st.download_button("Download HTML", html, file_name="resume.html", mime="text/html")

    # PDF via wkhtmltopdf (installed via packages.txt)
    try:
        import pdfkit  # ✅ import here to avoid startup crashes
        # Let pdfkit auto-detect Linux wkhtmltopdf installed by packages.txt
        pdf_path = "resume.pdf"
        pdfkit.from_string(html, pdf_path)  # no Windows path, no config needed
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="resume.pdf", mime="application/pdf")
    except Exception as e:
        st.warning("PDF export is temporarily unavailable. HTML and DOCX downloads still work.")
        st.caption(f"Details: {e}")

    # DOCX
    docx_path = "resume.docx"
    export_docx(name, email, phone, summary, skills_list, experience, education, docx_path)
    with open(docx_path, "rb") as f:
        st.download_button(
            "Download DOCX",
            f,
            file_name="resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # Match score
    if job_description.strip():
        resume_text = f"{summary} {', '.join(skills_list)} {experience} {education}"
        score = match_score(resume_text, job_description)
        st.markdown(f"### 📊 Job Match Score: {score}%")
