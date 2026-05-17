import os
import joblib

from flask import current_app

from app.utils.logger import (
    logger
)


# =====================================================
# ML Models
# =====================================================

score_model = None

duration_model = None


# =====================================================
# Load ML Models
# =====================================================

def load_ml_models():

    global score_model
    global duration_model

    try:

        score_model_path = current_app.config[
            "SCORE_MODEL_PATH"
        ]

        duration_model_path = current_app.config[
            "DURATION_MODEL_PATH"
        ]

        # =============================================
        # Check Files Exist
        # =============================================

        if not os.path.exists(
            score_model_path
        ):

            logger.warning(

                "Score model not found: %s",

                score_model_path
            )

            return

        if not os.path.exists(
            duration_model_path
        ):

            logger.warning(

                "Duration model not found: %s",

                duration_model_path
            )

            return

        # =============================================
        # Load Models
        # =============================================

        score_model = joblib.load(
            score_model_path
        )

        duration_model = joblib.load(
            duration_model_path
        )

        logger.info(
            "ML models loaded successfully."
        )

    except Exception as e:

        logger.exception(

            "Failed loading ML models: %s",

            str(e)
        )


# =====================================================
# Get Score Model
# =====================================================

def get_score_model():

    return score_model


# =====================================================
# Get Duration Model
# =====================================================

def get_duration_model():

    return duration_model


# =====================================================
# Check Models Loaded
# =====================================================

def models_loaded():

    return (

        score_model is not None

        and

        duration_model is not None
    )