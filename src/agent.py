"""
----------------------------------
basic tool-calling demonstration:
---------------------------------

Give Tools to Agent:-
                    AI AGENT
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
Placement Tool   Resume Tool      Skill Gap Tool
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                    RAG Tool

The important part is:
You don't tell the Agent which tool to use for every question.

You give the Agent all available tools.
The LLM decides which tool is appropriate based on the student's question.

----

Student asks:

"Analyze my resume and tell me whether I'm ready for a Data Scientist job."

Agent can decide:

1. Read resume
2. Extract skills
3. Check skill gaps
4. Run ML placement prediction
5. Search relevant jobs
6. Generate final recommendation

This is much closer to real Agentic AI.
"""

import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool

from src.predict import predict_placement
from src.skill_gap import find_missing_skills
from src.rag import ask_question


# Load environment variables
load_dotenv()


# ============================================================
# 1. Placement Prediction Tool
# ============================================================

@tool
def placement_prediction(cgpa: float):
    """
    Predict the student's placement package using CGPA.
    """

    result = predict_placement(cgpa=cgpa)

    return str(result)


# ============================================================
# 2. Skill Gap Tool
# ============================================================

@tool
def skill_gap_analysis(student_skills: str):
    """
    Find missing skills for a Data Scientist career.
    """

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

    student_skill_list = [skill.strip() for skill in student_skills.split(",")]
    missing_skills = find_missing_skills(
        student_skill_list,
        required_skills
    )

    return str(missing_skills)


# ============================================================
# 3. Career RAG Tool
# ============================================================

@tool
def career_knowledge_search(question: str):
    """
    Search the career knowledge base and answer the question.
    """

    answer = ask_question(question)

    return answer


# ============================================================
# 4. Create Tools List
# ============================================================

tools = [
    placement_prediction,
    skill_gap_analysis,
    career_knowledge_search
]


# ============================================================
# 5. Create AI Agent
# ============================================================

def create_agent():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools


# ============================================================
# 6. Ask Agent
# ============================================================

def ask_agent(question):

    agent = create_agent()

    # First ask LLM which tool to use
    response = agent.invoke(question)

    # If LLM does not select a tool
    if not response.tool_calls:
        return response.content

    # Execute selected tool
    tool_results = []

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        for tool in tools:
            if tool.name == tool_name:
                result = tool.invoke(tool_args)
                tool_results.append(str(result))

    # Send tool result back to LLM
    final_question = f"""
You are an AI Student Career Assistant.

Student Question:
{question}

Tool Result:
{tool_results}

Give the final answer to the student
in simple and clear language.
"""

    final_response = agent.invoke(final_question)
    return final_response


# ============================================================
# 7. Test Agent
# ============================================================

if __name__ == "__main__":

    question = input("\nAsk your career question: ")
    response = ask_agent(question)
    print("\nAgent Response:")
    print(response.content)