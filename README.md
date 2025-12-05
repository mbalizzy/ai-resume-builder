# 📄 AI Resume Builder

An interactive web app built with **Streamlit** that helps users generate professional resumes in multiple formats (HTML, PDF, DOCX) and evaluate job description match scores using AI.

---

## 🚀 Live Demo
👉 [Try the app here](https://ai-resume-builder-hswd4t6nhknrjfpbvpb4pq.streamlit.app)

---

## ✨ Features
- **Interactive form**: Enter personal details, skills, experience, and education.
- **Template selection**: Choose from multiple resume templates.
- **Resume preview**: See your resume styled in real time.
- **Export options**:
  - Download as **HTML**
  - Download as **PDF**
  - Download as **DOCX**
- **Job match score**: Paste a job description and get a similarity score.

---

## 🧪 Sample Data for Testing
Use this example to quickly test the app:

- **Full Name**: Thando Mkhize  
- **Email**: thando.mkhize@example.com  
- **Phone Number**: +27 82 456 7890  
- **Professional Summary**: Results-driven data analyst with 3+ years of experience in transforming complex datasets into actionable insights.  
- **Skills**: Python, SQL, Streamlit, Power BI, Excel, Machine Learning, Data Visualization  
- **Work Experience**:  
  - Data Analyst at Nedbank (2022–2025)  
  - Junior Analyst at CAPACITI (2021–2022)  
- **Education**:  
  - BSc in Statistics and Computer Science, UKZN  
  - CAPACITI Data Science Programme  
- **Job Description**: Seeking a data analyst with strong Python and dashboarding skills to support our BI team.

---

## ⚙️ Tech Stack
- **Streamlit** – interactive web UI
- **Jinja2** – HTML templating
- **pdfkit / wkhtmltopdf** – PDF export
- **python-docx** – DOCX export
- **scikit-learn** – job match scoring

---

## 📂 Project Setup
Clone the repo and install dependencies:

```bash
git clone https://github.com/mbalizzy/ai-resume-builder.git
cd ai-resume-builder
pip install -r requirements.txt
streamlit run app.py
