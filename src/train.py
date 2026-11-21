import json
import joblib
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from src.config import (
    TRAIN_DATA,
    TEST_DATA,
    MODEL_PATH,
    REPORTS_DIR,
    METRICS_PATH
)


def train_model():

    # 1. Load processed data
    train_data = pd.read_csv(TRAIN_DATA)
    test_data = pd.read_csv(TEST_DATA)

    # 2. Separate X and y
    X_train = train_data.drop(columns="package")
    y_train = train_data["package"]

    X_test = test_data.drop(columns="package")
    y_test = test_data["package"]

    # 3. Define optimized regression models
    models = {
        "Linear Regression": LinearRegression(),
        
        "Ridge Regression": Ridge(alpha=1.0),

        "KNN Regressor": KNeighborsRegressor(n_neighbors=5, weights="uniform"),

        "SVR (RBF Kernel)": SVR(kernel="rbf", C=5.0, epsilon=0.05),

        "SVR (Linear Kernel)": SVR(kernel="linear", C=1.0, epsilon=0.1),

        "Random Forest": RandomForestRegressor( n_estimators=200, max_depth=4, random_state=42 )
    }

    results = {}
    best_r2 = -float("inf")
    best_model_name = None
    best_model_instance = None

    # 4. Train and evaluate models
    for name, model in models.items():

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        }

        print(f"\n{name}")
        print("MAE:", mae)
        print("MSE:", mse)
        print("RMSE:", rmse)
        print("R2 Score:", r2)

        # Track the actual best model based on R2 Score
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model_instance = model

    print(f"\n🏆 Best Model Selected: {best_model_name} (R2: {best_r2:.4f})")

    # 5. Create models folder
    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # 6. Save the actual best model
    joblib.dump(
        best_model_instance,
        MODEL_PATH
    )

    # 7. Create reports folder
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # 8. Save metrics
    with open(METRICS_PATH, "w") as file:
        json.dump(
            results,
            file,
            indent=4
        )

    print("\nModel saved successfully!")
    print("Model path:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
