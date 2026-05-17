import logging

from config import Config


# =====================================================
# Configure Logger
# =====================================================

logging.basicConfig(

    level=Config.LOG_LEVEL,

    format=Config.LOG_FORMAT
)


# =====================================================
# Main Logger
# =====================================================

logger = logging.getLogger(
    "major_project"
)