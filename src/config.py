from pathlib import Path


# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent


# Data paths
RAW_DATA = ROOT_DIR / "data" / "raw" / "placement.csv"

PROCESSED_DIR = ROOT_DIR / "data" / "processed"

TRAIN_DATA = PROCESSED_DIR / "train_processed.csv"

TEST_DATA = PROCESSED_DIR / "test_processed.csv"


# Model path
MODEL_PATH = ROOT_DIR / "models" / "placement_model.pkl"

PREPROCESSOR_PATH = ROOT_DIR / "models" / "preprocessor.joblib"

# Reports
REPORTS_DIR = ROOT_DIR / "reports"

METRICS_PATH = REPORTS_DIR / "metrics.json"


#-------------------------------------------------

# Project root: 
# 1_AI_Student_Career_and_Placement_Assistant/ 
PROJECT_ROOT = Path(__file__).resolve().parent.parent 

# Knowledge base folder 
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledge_base" 

# Chroma vector database folder 
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"

#---------------------------------------------------

