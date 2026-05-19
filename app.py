from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pdf2image 
load_dotenv()
import base64
import io

api_key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def get_gemini_response(input_text,pdf_content,prompt):
    client=genai.Client()   
    model=genai.GenerativeModel('gemini-3.1-pro-preview')
    response=model.generate_content([input_text,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read(),
            poppler_path=r"C:\poppler\poppler-26.02.0\Library\bin")
        
        pdf_parts=[]

        for page in images:
            img_byte_arr = io.BytesIO()
            page.save(img_byte_arr, format='JPEG')
        
        pdf_parts.append(
        {
            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr.getvalue()).decode()
        }
        )

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="ATS Resume Analyzer",page_icon=":guardsman:",layout="wide")
st.header("ATS Tracking System")
input_text=st.text_area("JOb Description: ",height=200,key="input")
uploaded_file=st.file_uploader("Upload Resume here....(PDF) ",type=['pdf'])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1=st.button("Tell me about the resume")
#submit2=st.button("How can I improve my resume or skills?")
submit3=st.button("What percentage of the job description does my resume match?")
submit4 = st.button("Extract Skills")

input_prompt1="""
You are an experienced HR with Technical Experience in the field of Data Science, Full Stack Web Development, 
and DEVOPS, Data Analyst. Your task is to analyze the resume provided in the PDF and provide a detailed summary of 
the candidate's qualifications, skills, and experience. Also share your professional evaluation on whether the 
candidate's profile aligns with the job description provided.
Highlight any relevant achievements or projects that demonstrate the candidate's suitability for roles in Data Science,
Full Stack Development, DEVOPS and Data Analyst.

"""
input_prompt3 = """
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

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Response is...")
        st.write(response)
    else:
        st.error("Please upload a PDF file to analyze.")
if submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Response is...")
        st.write(response)
    else:
        st.error("Please upload a PDF file to analyze.")

        

