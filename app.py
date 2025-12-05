import streamlit as st
from jinja2 import Environment, FileSystemLoader
# import pdfkit   # ❌ Commented out: causes wkhtmltopdf errors on Streamlit Cloud
import os
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import shutil   # ❌ Not needed anymore

# ❌ Commented out: wkhtmltopdf detection/configuration (not available on Streamlit Cloud)
# WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# WKHTMLTOPDF_EXISTS = bool(shutil.which("wkhtmltopdf")) or os.path.exists(WKHTMLTOPDF_PATH)
# if WKHTMLTOPDF_EXISTS:
#     config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH) if os.path.exists(WKHTMLTOPDF_PATH) else pdfkit.configuration()
# else:
#     config = None
# path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# ✅ Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

# ✅ DOCX export helper
def export_docx(name, email, phone, summary, skills, experience, education, output_path):
    doc = Document()
    doc.add_heading(name, 0)
    doc.add_paragraph(f"Email: {email}")
    doc.add_paragraph(f"Phone: {phone}")

    doc.add_heading("Professional Summary", level=1)
    doc.add_paragraph(summary)

    doc.add_heading("Key Skills", level=1)
    for skill in skills:
        doc.add_paragraph(skill, style="List Bullet")

    doc.add_heading("Work Experience", level=1)
    doc.add_paragraph(experience)

    doc.add_heading("Education", level=1)
    doc.add_paragraph(education)

    doc.save(output_path)

# ✅ Job description match score
def match_score(resume_text, job_text):
    vectorizer = TfidfVectorizer().fit([resume_text, job_text])
    vectors = vectorizer.transform([resume_text, job_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

# ✅ Streamlit page setup
st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder")

# ✅ Input form
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
    submitted = st.form_submit_button("Generate Resume")

# ✅ WeasyPrint integration
from weasyprint import HTML

def export_resume_to_pdf(template_name, context, output_path="resume.pdf"):
    template = env.get_template(template_name)
    html_content = template.render(context)
    HTML(string=html_content).write_pdf(output_path)

if submitted:
    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
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

    # Preview in Streamlit
    st.markdown("### 💡 Resume Preview")
    st.components.v1.html(html, height=800, scrolling=True)

    # Export options
    st.markdown("### 📥 Download Options")

    # HTML download
    st.download_button("Download HTML", html, file_name="resume.html", mime="text/html")

    # ✅ PDF export using WeasyPrint
    pdf_path = "resume.pdf"
    context = {
        "name": name,
        "email": email,
        "phone": phone,
        "summary": summary,
        "skills": skills_list,
        "experience": experience,
        "education": education
    }
    export_resume_to_pdf(template_choice, context, pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="resume.pdf", mime="application/pdf")

    # ✅ DOCX export
    docx_path = "resume.docx"
    export_docx(name, email, phone, summary, skills_list, experience, education, docx_path)
    with open(docx_path, "rb") as f:
        st.download_button("Download DOCX", f, file_name="resume.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # ✅ Job description match score
    if job_description.strip():
        resume_text = f"{summary} {', '.join(skills_list)} {experience} {education}"
        score = match_score(resume_text, job_description)
        st.markdown(f"### 📊 Job Match Score: {score}%")
