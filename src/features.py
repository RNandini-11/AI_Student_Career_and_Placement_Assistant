import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures # 1. Added PolynomialFeatures

from src.config import RAW_DATA, PROCESSED_DIR, TRAIN_DATA, TEST_DATA, PREPROCESSOR_PATH


def create_features():

    # Load dataset
    df = pd.read_csv(RAW_DATA)
    df = df.drop_duplicates()

    # Feature Engineering
    df["cgpa_squared"] = df["cgpa"] ** 2

    # Separate input and target
    X = df.drop("package", axis=1)
    y = df["package"]

    numerical_columns = ["cgpa", "cgpa_squared"]

    # 2. Add Polynomial Features (degree=2) into the pipeline before scaling
    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    preprocessor = ColumnTransformer([
        ("numerical", numerical_pipeline, numerical_columns)
    ])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Save the same preprocessor used during training
    joblib.dump(
        preprocessor,
        PREPROCESSOR_PATH
    )

    feature_names = ["cgpa", "cgpa_squared"]

    X_train_processed = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_processed = pd.DataFrame(X_test_processed, columns=feature_names)

    # Add target column back
    X_train_processed["package"] = y_train.values
    X_test_processed["package"] = y_test.values

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    X_train_processed.to_csv(TRAIN_DATA, index=False)
    X_test_processed.to_csv(TEST_DATA, index=False)

    print("\n✨ Feature engineering completed successfully!\n")


if __name__ == "__main__":
    create_features()
