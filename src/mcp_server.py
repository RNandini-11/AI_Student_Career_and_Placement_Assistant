from mcp.server.fastmcp import FastMCP

from src.predict import predict_placement
from src.skill_gap import find_missing_skills
from src.rag import ask_question


# ============================================================
# Create MCP Server
# ============================================================

mcp = FastMCP(
    "AI Career Assistant"
)


# ============================================================
# Tool 1: Placement Prediction
# ============================================================

@mcp.tool()
def predict_student_package(cgpa: float) -> str:
    """
    Predict the student's placement package using CGPA.
    """


    result = predict_placement(
        cgpa=cgpa
    )

    return str(result)


# ============================================================
# Tool 2: Skill Gap Analysis
# ============================================================

@mcp.tool()
def find_skill_gap(student_skills: str) -> str:
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

    student_skill_list = [
        skill.strip()
        for skill in student_skills.split(",")
    ]

    missing_skills = find_missing_skills(
        student_skill_list,
        required_skills
    )

    return str(missing_skills)


# ============================================================
# Tool 3: Career Knowledge / RAG
# ============================================================

@mcp.tool()
def career_knowledge(question: str) -> str:
    """
    Search the career knowledge base and answer the question.
    """

    answer = ask_question(
        question
    )

    return answer


# ============================================================
# Run MCP Server
# ============================================================

if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )