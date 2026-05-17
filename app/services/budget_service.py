import pandas as pd

from flask import current_app


# =====================================================
# Generate Budget Plan
# =====================================================

def generate_budget_plan(data):

    budget = float(
        data.get("budget", 0)
    )

    days = int(
        data.get("days", 1)
    )

    people = int(
        data.get("people", 1)
    )

    state = data.get(
        "state",
        ""
    ).strip().lower()

    city = data.get(
        "city",
        ""
    ).strip().lower()

    # =============================================
    # Load Dataset
    # =============================================

    df = pd.read_csv(

        current_app.config[
            "BUDGET_DATASET"
        ]
    )

    # =============================================
    # Normalize
    # =============================================

    df.columns = [

        c.strip()

        for c in df.columns
    ]

    # =============================================
    # Filtering
    # =============================================

    if "State" in df.columns:

        df = df[
            df["State"]
            .astype(str)
            .str.lower()
            .str.contains(
                state,
                na=False
            )
        ]

    if city and "City" in df.columns:

        df = df[
            df["City"]
            .astype(str)
            .str.lower()
            .str.contains(
                city,
                na=False
            )
        ]

    # =============================================
    # Budget Calculation
    # =============================================

    if "EstimatedBudget" in df.columns:

        df = df[
            df["EstimatedBudget"]
            <= budget
        ]

    # =============================================
    # Days Matching
    # =============================================

    if "RecommendedDays" in df.columns:

        df = df[
            df["RecommendedDays"]
            <= days
        ]

    # =============================================
    # Limit Results
    # =============================================

    df = df.head(15)

    # =============================================
    # Final Result
    # =============================================

    return {

        "success": True,

        "count": len(df),

        "results":
            df.to_dict(
                orient="records"
            )
    }