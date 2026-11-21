import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.predict import predict_placement
from src.resume_extractor import extract_resume_text
from src.skill_gap import extract_skills, find_missing_skills

from src.rag import ask_question
from src.agent import ask_agent


app = FastAPI(
    title="AI Student Career Assistant API",
    description="Backend API for the AI Student Career and Placement Assistant",
    version="1.0.0"
)


# Request Models
class StudentInput(BaseModel):
    cgpa: float

class SkillGapInput(BaseModel):
    student_skills: list[str]

class CareerQuestionInput(BaseModel):
    question: str

class AgentInput(BaseModel):
    question: str


#  Check API
@app.get("/")
def home():
    return {
        "message": "AI Student Career Assistant API is running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Predict package from CGPA
@app.post("/predict")
def predict_package(student: StudentInput):

    result = predict_placement(
        cgpa=student.cgpa
    )

    return result


# Upload PDF → Extract text → Find skills
@app.post("/resume-analysis")
# FastAPI + file upload + temporary file + PDF processing
# File() --> tells FastAPI this input is a file
# async, await --> handle waiting operations efficiently
async def resume_analysis(file: UploadFile = File(...)):
    #file validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    # temporarily save the PDF
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        # Read uploaded file
        contents = await file.read()
        # Save the PDF temporarily
        temp_file.write(contents)
        temp_file_path = temp_file.name

    try:
        resume_text = extract_resume_text(temp_file_path)
        skills = extract_skills(resume_text)

        return {
            "filename": file.filename,
            "resume_text": resume_text,
            "skills_found": skills
        }

    finally:

        os.remove(temp_file_path)


# Find missing skills
@app.post("/skill-gap")
def skill_gap(data: SkillGapInput):

    required_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Power BI",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Statistics"
    ]

    missing_skills = find_missing_skills(
        data.student_skills,
        required_skills
    )

    return {
        "student_skills": data.student_skills,
        "required_skills": required_skills,
        "missing_skills": missing_skills
    }

# Ask RAG question
@app.post("/career-question")
def career_question(data: CareerQuestionInput):

    answer = ask_question(
        data.question
    )

    return {
        "question": data.question,
        "answer": answer
    }


# Ask AI agent
@app.post("/agent")
async def agent(data: AgentInput):

    response = ask_agent(
        data.question
    )

    return {
        "question": data.question,
        "response": response.content
    }

