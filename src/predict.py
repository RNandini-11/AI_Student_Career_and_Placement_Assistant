import joblib
import pandas as pd
from src.config import MODEL_PATH, PREPROCESSOR_PATH


def predict_placement(cgpa):

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Load same preprocessor used during training
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    # Student data 
    student = pd.DataFrame({
            "cgpa": [cgpa],
            "cgpa_squared": [cgpa ** 2]
        }, columns=["cgpa", "cgpa_squared"])

    # Apply same preprocessing
    student_processed = preprocessor.transform(student)

    student_processed = pd.DataFrame(student_processed, columns=["cgpa", "cgpa_squared"])

    # Prediction
    prediction = model.predict(student_processed)

    # Predicted package
    predicted_package = prediction[0]

    return {
        "prediction": round(
            predicted_package,
            2
        )
    }

if __name__ == "__main__":

    #result = predict_placement(

    #     cgpa=5.0,
    #    cgpa_squared=25.0

    #)

    for cgpa in [3.0, 5.0, 7.0, 8.2, 9.0]:

        result = predict_placement(cgpa)

        print(
            f"{cgpa} CGPA → "
            f"{result['prediction']} LPA"
        )

    #print("\nPrediction Result:")
    #print(f"Predicted Package: {result['prediction']} LPA\n")

