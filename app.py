import asyncio
import tempfile

import streamlit as st

from src.predict import predict_placement
from src.resume_extractor import extract_resume_text
from src.resume_analyzer import analyze_resume
from src.skill_gap import (
    extract_skills,
    find_missing_skills
)
from src.rag import ask_question
from src.agent import ask_agent


# Page Configuration----------------------------------------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🎓",
    layout="wide"
)


# Title------------------------------------------------------------
st.title("🎓 AI Student Career & Placement Assistant")

st.write(
    "An AI assistant for placement prediction, "
    "resume analysis, skill gap analysis and career guidance."
)


# Sidebar----------------------------------------------------------
st.sidebar.title("Student Information")

cgpa = st.sidebar.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    value=8.0,
    step=0.1
)


student_skills = st.sidebar.text_area(
    "Your Skills",
    placeholder="Python, SQL, Power BI"
)


# Tabs---------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Placement Prediction",
        "📄 Resume Analysis",
        "📚 Career RAG",
        "🤖 AI Agent"
    ]
)


# 36. Connect ML Model----------------------------------------------
with tab1:

    st.header("📊 Placement Package Prediction")
    st.write("Enter your CGPA to predict the expected package.")

    if st.button("Predict Package"):

        result = predict_placement(
            cgpa=cgpa
          
        )

        st.success(
            f"Predicted Package: "
            f"{result['prediction']} LPA"
        )


# 37. Connect Resume Analyzer----------------------------------------
with tab2:

    st.header("📄 Resume Analyzer")

    uploaded_resume = st.file_uploader(
        "Upload your Resume PDF",
        type=["pdf"]
    )

    if uploaded_resume:

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_resume.getvalue())
            pdf_path = temp_file.name

        # Extract Resume Text--------------------------------------
        resume_text = extract_resume_text(pdf_path)
        st.subheader("Extracted Resume Text")

        st.text_area(
            "Resume Text",
            resume_text,
            height=250
        )

        # Transformer Analysis---------------------------------------
        if st.button("Analyze Resume"):
            cleaned_text = resume_text.lower()
            transformer_results = analyze_resume(cleaned_text)
            st.subheader("Transformer Analysis")

            for result in transformer_results:
                st.write(result)

            # Skill Extraction--------------------------------------
            skills = extract_skills(resume_text)
            st.subheader("Technical Skills Found")
            if skills:
                for skill in skills:
                    st.write(f"✅ {skill}")
            else:
                st.warning("No predefined technical skills found.")

            # Skill Gap---------------------------------------------
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
                skills,
                required_skills
            )

            st.subheader("Skill Gap")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"❌ {skill}")
            else:
                st.success("No major skill gaps found!")


# 38. Connect RAG---------------------------------------------------
with tab3:

    st.header("📚 Career Knowledge Assistant")

    question = st.text_area(
        "Ask a career question",
        placeholder=(
            "What should I learn to become "
            "a Data Scientist?"
        )
    )

    if st.button("Ask Career Assistant"):
        if question:
            with st.spinner("Searching career knowledge..."):
                answer = ask_question(question)
            st.subheader("Answer")
            st.write(answer)

        else:
            st.warning("Please enter a question.")


# 39 + 40. Connect Agent + MCP----------------------------------------
with tab4:

    st.header("🤖 AI Career Agent")

    st.write(
        "The AI Agent can decide which MCP tool "
        "should be used."
    )

    agent_question = st.text_area(
        "Ask the AI Agent",
        placeholder=("Predict my package for 8.2 CGPA")
    )

    if st.button("Ask AI Agent"):

        if agent_question:
            with st.spinner("AI Agent is thinking..."):
                response = ask_agent(agent_question)

            st.subheader("AI Agent Response")
            st.success(response.content)

        else:
            st.warning("Please enter a question.")



# Footer-------------------------------------------------------
st.divider()

st.caption(
    "AI Student Career & Placement Assistant | "
    "Python + ML + DL + GenAI + RAG + Agentic AI + MCP"
)