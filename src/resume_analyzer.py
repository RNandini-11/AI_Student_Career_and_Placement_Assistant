# Now we bring the pretrained Transformer into the project.
# We can use a pretrained Named Entity Recognition (NER) model.
#------------------------------------------------------------------

import re
from transformers import pipeline


def preprocess_text(text):
    
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def create_resume_analyzer():
    analyzer = pipeline(
        "ner",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple"
    )
    return analyzer


def analyze_resume(resume_text):
    analyzer = create_resume_analyzer()
    results = analyzer(resume_text)
    return results


if __name__ == "__main__":

    resume_text = """
    Rajnandini Deshmukh from Baramati. 
    I worked as a PowerBI Intern at Cognifyz Technologies and a Data Science Intern at Oasis Infobyte.
    I have experience in Python, SQL, and Power BI.
    """

    # Preprocess text (Preserving Capitalization)
    cleaned_text = preprocess_text(resume_text)

    # Transformer analysis
    results = analyze_resume(cleaned_text)

    print("\nTransformer Output:\n")
    
    if not results:
        print("No entities found by the model.")
    else:
        for result in results:
            print(result)
