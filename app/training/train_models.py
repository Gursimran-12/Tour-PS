import os
import joblib
import sklearn
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.compose import (
    ColumnTransformer
)

from sklearn.metrics import (
    mean_absolute_error
)

from sklearn.preprocessing import (

    OneHotEncoder,

    StandardScaler
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.model_selection import (
    train_test_split
)


# =====================================================
# Base Paths
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV = os.path.join(
    BASE_DIR,
    "places_dataset.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "..",
    "ml_models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# =====================================================
# Validate Dataset
# =====================================================

if not os.path.exists(CSV):

    raise FileNotFoundError(

        f"{CSV} not found."
    )


print(
    f"Using dataset: {CSV}"
)

print(
    f"scikit-learn version: "
    f"{sklearn.__version__}"
)


# =====================================================
# Load Dataset
# =====================================================

df = pd.read_csv(CSV)


# =====================================================
# Convert Time to Minutes
# =====================================================

def time_to_min(t):

    try:

        h, m = map(
            int,
            str(t).split(":")
        )

        return h * 60 + m

    except Exception:

        return np.nan


# =====================================================
# Time Features
# =====================================================

df["opening_min"] = df.get(
    "Opening_Time",
    np.nan
).apply(time_to_min)

df["closing_min"] = df.get(
    "Closing_Time",
    np.nan
).apply(time_to_min)

df["open_duration_min"] = (

    df["closing_min"]

    -

    df["opening_min"]
)


# =====================================================
# Features
# =====================================================

numeric_features = [

    "Google_Rating",

    "Google_Reviews_Lakh",

    "Entrance_Fee_INR",

    "Established_Year",

    "opening_min",

    "closing_min",

    "open_duration_min",

    "Avg_Visit_Duration_hr"
]

categorical_features = [

    "Category",

    "Significance",

    "City",

    "State",

    "Zone",

    "Airport_within_50km",

    "Weekly_Off",

    "DSLR_Allowed",

    "Best_Time_to_Visit"
]


# =====================================================
# Numeric Cleanup
# =====================================================

for col in numeric_features:

    if col not in df.columns:

        df[col] = np.nan

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# =====================================================
# Categorical Cleanup
# =====================================================

for col in categorical_features:

    if col not in df.columns:

        df[col] = "Unknown"

    df[col] = df[col].fillna(
        "Unknown"
    ).astype(str)


# =====================================================
# Targets
# =====================================================

target_score_col = (
    "Popularity_Score"
)

target_duration_col = (
    "Avg_Visit_Duration_min"
)


# =====================================================
# Validate Targets
# =====================================================

if (

    target_score_col not in df.columns

    or

    target_duration_col not in df.columns
):

    raise KeyError(

        f"Missing target columns. "

        f"Need "

        f"'{target_score_col}' "

        f"and "

        f"'{target_duration_col}'."
    )


# =====================================================
# Remove Invalid Rows
# =====================================================

df = df.dropna(

    subset=[

        target_score_col,

        target_duration_col
    ]
)


# =====================================================
# Fill Numeric NaNs
# =====================================================

for col in numeric_features:

    df[col] = df[col].fillna(
        df[col].median()
    )


# =====================================================
# Input Features
# =====================================================

X = df[
    numeric_features
    +
    categorical_features
]

y_score = df[
    target_score_col
].astype(float)

y_duration = df[
    target_duration_col
].astype(float)


# =====================================================
# Train Test Split
# =====================================================

X_train, X_test, ys_train, ys_test = train_test_split(

    X,
    y_score,

    test_size=0.2,

    random_state=42
)

_, _, yd_train, yd_test = train_test_split(

    X,
    y_duration,

    test_size=0.2,

    random_state=42
)


# =====================================================
# sklearn Compatibility
# =====================================================

sk_version = tuple(

    map(
        int,
        sklearn.__version__.split(".")[:2]
    )
)

if sk_version >= (1, 4):

    cat_enc = OneHotEncoder(

        handle_unknown="ignore",

        sparse_output=False
    )

else:

    cat_enc = OneHotEncoder(

        handle_unknown="ignore",

        sparse=False
    )


# =====================================================
# Preprocessor
# =====================================================

preprocessor = ColumnTransformer(

    transformers=[

        (

            "num",

            StandardScaler(),

            numeric_features
        ),

        (

            "cat",

            cat_enc,

            categorical_features
        )
    ],

    remainder="drop"
)


# =====================================================
# Score Model Pipeline
# =====================================================

score_pipeline = Pipeline([

    (
        "pre",
        preprocessor
    ),

    (
        "model",

        RandomForestRegressor(

            n_estimators=150,

            random_state=42,

            n_jobs=-1
        )
    )
])


# =====================================================
# Duration Model Pipeline
# =====================================================

duration_pipeline = Pipeline([

    (
        "pre",
        preprocessor
    ),

    (
        "model",

        RandomForestRegressor(

            n_estimators=150,

            random_state=42,

            n_jobs=-1
        )
    )
])


# =====================================================
# Train Models
# =====================================================

print(
    "Training score model..."
)

score_pipeline.fit(
    X_train,
    ys_train
)

print(
    "Training duration model..."
)

duration_pipeline.fit(
    X_train,
    yd_train
)


# =====================================================
# Predictions
# =====================================================

pred_score = score_pipeline.predict(
    X_test
)

pred_duration = duration_pipeline.predict(
    X_test
)


# =====================================================
# Metrics
# =====================================================

print(

    "MAE score:",

    mean_absolute_error(

        ys_test,

        pred_score
    )
)

print(

    "MAE duration (min):",

    mean_absolute_error(

        yd_test,

        pred_duration
    )
)


# =====================================================
# Save Models
# =====================================================

score_model_path = os.path.join(

    MODEL_DIR,

    "score_model.joblib"
)

duration_model_path = os.path.join(

    MODEL_DIR,

    "duration_model.joblib"
)

joblib.dump(

    score_pipeline,

    score_model_path
)

joblib.dump(

    duration_pipeline,

    duration_model_path
)


# =====================================================
# Done
# =====================================================

print(
    "\nModels saved successfully:"
)

print(
    f"Score Model: {score_model_path}"
)

print(
    f"Duration Model: {duration_model_path}"
)