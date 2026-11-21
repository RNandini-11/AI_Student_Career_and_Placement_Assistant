def extract_skills(resume_text):

    skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Power BI",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "NLP",
        "Statistics",
        "Excel",
        "Tableau"
    ]

    resume_text = resume_text.lower()

    found_skills = []

    for skill in skills:

        if skill.lower() in resume_text:

            found_skills.append(skill)

    return found_skills


def find_missing_skills(
    student_skills,
    required_skills
):

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in [
            s.lower()
            for s in student_skills
        ]:

            missing_skills.append(skill)

    return missing_skills


if __name__ == "__main__":

    resume_text = """
    Python SQL Machine Learning
    Power BI Pandas
    """

    student_skills = extract_skills(
        resume_text
    )

    required_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "NLP"
    ]

    missing_skills = find_missing_skills(
        student_skills,
        required_skills
    )

    print("\nStudent Skills:")
    print(student_skills)

    print("\nMissing Skills:")
    print(missing_skills)