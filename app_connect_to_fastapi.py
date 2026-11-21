import requests
import streamlit as st

# Base URL of your running FastAPI server
API_URL = "http://127.0.0.1:8000"

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
        with st.spinner("Fetching prediction from server..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"cgpa": cgpa}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(
                        f"Predicted Package: "
                        f"{result['prediction']} LPA"
                    )
                else:
                    st.error(f"Failed to get prediction from FastAPI. Status code: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI server. Ensure uvicorn is running on port 8000.")

# 37. Connect Resume Analyzer----------------------------------------
with tab2:
    st.header("📄 Resume Analyzer")

    uploaded_resume = st.file_uploader(
        "Upload your Resume PDF",
        type=["pdf"]
    )

    if uploaded_resume:
        # Note: PDF temporary file storage is now fully handled by FastAPI behind the scenes!
        if st.button("Analyze Resume"):
            files = {
                "file": (
                    uploaded_resume.name,
                    uploaded_resume.getvalue(),
                    "application/pdf"
                )
            }
            
            with st.spinner("Analyzing resume content via server..."):
                try:
                    # 1. Hit the primary resume analysis endpoint
                    resume_response = requests.post(
                        f"{API_URL}/resume-analysis",
                        files=files
                    )
                    
                    if resume_response.status_code == 200:
                        resume_result = resume_response.json()
                        resume_text = resume_result.get("resume_text", "")
                        skills = resume_result.get("skills_found", [])
                        
                        # Display Extracted Text
                        st.subheader("Extracted Resume Text")
                        st.text_area(
                            "Resume Text",
                            resume_text,
                            height=250
                        )
                        
                        # Transformer Analysis (Handled as part of the analysis payload)
                        st.subheader("Transformer Analysis")
                        transformer_results = resume_result.get("transformer_analysis", [])
                        if transformer_results:
                            for result in transformer_results:
                                st.write(result)
                        else:
                            st.info("No explicit transformer text analysis classes returned.")

                        # Technical Skills Found
                        st.subheader("Technical Skills Found")
                        if skills:
                            for skill in skills:
                                st.write(f"✅ {skill}")
                        else:
                            st.warning("No predefined technical skills found.")

                        # 2. Automatically check for gaps using the specific /skill-gap endpoint
                        st.subheader("Skill Gap")
                        with st.spinner("Calculating matching gaps..."):
                            gap_response = requests.post(
                                f"{API_URL}/skill-gap",
                                json={"student_skills": skills}
                            )
                            
                            if gap_response.status_code == 200:
                                gap_result = gap_response.json()
                                missing_skills = gap_result.get("missing_skills", [])
                                
                                if missing_skills:
                                    for skill in missing_skills:
                                        st.write(f"❌ {skill}")
                                else:
                                    st.success("No major skill gaps found!")
                            else:
                                st.error("Failed to fetch Skill Gap data from API.")
                    else:
                        st.error(f"Resume analysis failed on FastAPI server. Status code: {resume_response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI server.")

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
                try:
                    response = requests.post(
                        f"{API_URL}/career-question",
                        json={"question": question}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("Answer")
                        st.write(result.get("answer", ""))
                    else:
                        st.error(f"Failed to query RAG model. Status code: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI server.")
        else:
            st.warning("Please enter a question.")

# 39 + 40. Connect Agent + MCP----------------------------------------
with tab4:
    st.header("🤖 AI Career Agent")
    st.write("The AI Agent can decide which MCP tool should be used.")

    agent_question = st.text_area(
        "Ask the AI Agent",
        placeholder=("Predict my package for 8.2 CGPA")
    )

    if st.button("Ask AI Agent"):
        if agent_question:
            with st.spinner("AI Agent is thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/agent",
                        json={"question": agent_question}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("AI Agent Response")
                        # Uses string values from the response payload key directly
                        st.success(result.get("response", ""))
                    else:
                        st.error(f"Agent processing error. Status code: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to FastAPI server.")
        else:
            st.warning("Please enter a question.")

# Footer-------------------------------------------------------
st.divider()

st.caption(
    "AI Student Career & Placement Assistant | "
    "Python + ML + DL + GenAI + RAG + Agentic AI + MCP + FastAPI + Docker"
)
