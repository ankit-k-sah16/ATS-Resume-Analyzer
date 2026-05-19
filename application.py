from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import pdf2image
import base64
import io

# =========================
# Load Environment Variables
# =========================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Google API Key not found. Please add it to your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# =========================
# Gemini Response Function
# =========================
def get_gemini_response(input_text, pdf_content, prompt):

    model = genai.GenerativeModel("gemini-3.1-flash-lite")

    response = model.generate_content(
        [prompt, input_text] + pdf_content
    )

    return response.text


# =========================
# PDF Processing Function
# =========================
def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:

        try:
            # Convert PDF to images
            images = pdf2image.convert_from_bytes(
                uploaded_file.read(),
                poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin"
                # Change this path according to your system
            )

            pdf_parts = []

            for page in images:

                img_byte_arr = io.BytesIO()

                page.save(img_byte_arr, format='JPEG')

                img_byte_arr = img_byte_arr.getvalue()

                pdf_parts.append(
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr).decode()
                    }
                )

            return pdf_parts

        except Exception as e:
            st.error(f"PDF Processing Error: {e}")
            return None

    else:
        st.error("No file uploaded")
        return None


# =========================
# Streamlit UI
# =========================
st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI ATS Resume Analyzer")

st.markdown("""
Analyze resumes against job descriptions using AI-powered ATS evaluation.
""")

# =========================
# Layout
# =========================
col1, col2 = st.columns(2)

with col1:

    input_text = st.text_area(
        "Paste Job Description",
        height=300,
        placeholder="Paste the complete job description here..."
    )

with col2:

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:
        st.success("Resume uploaded successfully ✅")


# =========================
# Buttons
# =========================
col3, col4, col5 = st.columns(3)

with col3:
    submit1 = st.button("Resume Summary")

with col4:
    submit2 = st.button("ATS Match Score")

with col5:
    submit3 = st.button("Skill Improvement Suggestions")


# =========================
# Prompts
# =========================
input_prompt1 = """
You are an experienced HR professional and technical recruiter.

Analyze the provided resume and provide:

1. Candidate Summary
2. Technical Skills
3. Experience Analysis
4. Project Analysis
5. Strengths
6. Weaknesses
7. Suitability for the provided job description
8. Final Evaluation

Provide the response in a structured format.
"""

input_prompt2 = """
You are a highly advanced Applicant Tracking System (ATS) and HR recruiter.

Analyze the provided resume against the job description.

Tasks:
1. Provide ATS Match Percentage
2. Identify missing keywords
3. Evaluate technical skills alignment
4. Evaluate project relevance
5. Evaluate resume formatting and ATS readability
6. Suggest concrete improvements
7. Highlight strengths
8. Provide final hiring recommendation

Return the output in clear sections.
"""

input_prompt3 = """
You are an expert career coach and resume reviewer.

Analyze the resume and provide:

1. Missing Skills
2. Important Technologies to Learn
3. Resume Improvement Suggestions
4. Better Resume Bullet Point Suggestions
5. ATS Optimization Tips
6. Interview Preparation Suggestions
7. Recommended Projects
8. Career Growth Suggestions

Provide detailed actionable feedback.
"""


# =========================
# Resume Summary
# =========================
if submit1:

    if uploaded_file is not None and input_text != "":

        with st.spinner("Analyzing Resume..."):

            pdf_content = input_pdf_setup(uploaded_file)

            if pdf_content:

                try:

                    response = get_gemini_response(
                        input_text,
                        pdf_content,
                        input_prompt1
                    )

                    st.subheader(" Resume Analysis")
                    st.write(response)

                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        st.warning("Please upload a resume and paste the job description.")


# =========================
# ATS Match Score
# =========================
if submit2:

    if uploaded_file is not None and input_text != "":

        with st.spinner("Calculating ATS Match Score..."):

            pdf_content = input_pdf_setup(uploaded_file)

            if pdf_content:

                try:

                    response = get_gemini_response(
                        input_text,
                        pdf_content,
                        input_prompt2
                    )

                    st.subheader("📊 ATS Match Analysis")
                    st.write(response)

                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        st.warning("Please upload a resume and paste the job description.")


# =========================
# Skill Improvement Suggestions
# =========================
if submit3:

    if uploaded_file is not None:

        with st.spinner("Generating Suggestions..."):

            pdf_content = input_pdf_setup(uploaded_file)

            if pdf_content:

                try:

                    response = get_gemini_response(
                        input_text,
                        pdf_content,
                        input_prompt3
                    )

                    st.subheader("🚀 Skill Improvement Suggestions")
                    st.write(response)

                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        st.warning("Please upload a resume.")


# =========================
# Footer
# =========================
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + Gemini AI")