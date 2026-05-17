import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:

    # =====================================================
    # Flask Core Configuration
    # =====================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "super_secret_key"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "True"
    ) == "True"

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            5000
        )
    )

    # =====================================================
    # Static & Template Folders
    # =====================================================

    STATIC_FOLDER = "static"

    TEMPLATE_FOLDER = "templates"

    # =====================================================
    # Upload Configuration
    # =====================================================

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "static/uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit

    # =====================================================
    # Session Configuration
    # =====================================================

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    SESSION_PERMANENT = False

    PERMANENT_SESSION_LIFETIME = 3600

    # =====================================================
    # MySQL Database Configuration
    # =====================================================

    MYSQL_HOST = os.getenv(
        "MYSQL_HOST",
        "localhost"
    )

    MYSQL_USER = os.getenv(
        "MYSQL_USER",
        "root"
    )

    MYSQL_PASSWORD = os.getenv(
        "MYSQL_PASSWORD",
        ""
    )

    MYSQL_DB = os.getenv(
        "MYSQL_DB",
        "Users"
    )

    MYSQL_CURSORCLASS = "DictCursor"

    # =====================================================
    # API KEYS
    # =====================================================

    GEOAPIFY_KEY = os.getenv(
        "GEOAPIFY_KEY",
        ""
    )

    OPENWEATHER_KEY = os.getenv(
        "OPENWEATHER_KEY",
        ""
    )

    SERPAPI_API_KEY = os.getenv(
        "SERPAPI_API_KEY",
        ""
    )

    # =====================================================
    # Dataset Paths
    # =====================================================

    DATA_FOLDER = "data"

    HOTELS_DATASET = os.path.join(
        DATA_FOLDER,
        "hotels.csv"
    )

    PLACES_DATASET = os.path.join(
        DATA_FOLDER,
        "places.csv"
    )

    SIGHTSEEING_DATASET = os.path.join(
        DATA_FOLDER,
        "indian_sightseeing_places.csv"
    )

    BUDGET_DATASET = os.path.join(
        DATA_FOLDER,
        "budget_trip_data.csv"
    )

    CULTURE_DATASET = os.path.join(
        DATA_FOLDER,
        "indian_states_culture_dataset.csv"
    )

    # =====================================================
    # ML Model Configuration
    # =====================================================

    MODEL_FOLDER = "ml_models"

    SCORE_MODEL_PATH = os.path.join(
        MODEL_FOLDER,
        "score_model.joblib"
    )

    DURATION_MODEL_PATH = os.path.join(
        MODEL_FOLDER,
        "duration_model.joblib"
    )

    # =====================================================
    # Cache Configuration
    # =====================================================

    CACHE_TTL_SECONDS = 60 * 60

    # =====================================================
    # Logging Configuration
    # =====================================================

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    LOG_FORMAT = (
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    )

    # =====================================================
    # Geoapify API Configuration
    # =====================================================

    GEOAPIFY_BASE_URL = (
        "https://api.geoapify.com"
    )

    GEOAPIFY_PLACE_LIMIT = 120

    GEOAPIFY_TIMEOUT = 15

    # =====================================================
    # OpenWeather API Configuration
    # =====================================================

    WEATHER_BASE_URL = (
        "https://api.openweathermap.org/data/2.5"
    )

    WEATHER_UNITS = "metric"

    WEATHER_TIMEOUT = 10

    # =====================================================
    # Overpass API Configuration
    # =====================================================

    OVERPASS_API_URL = (
        "https://overpass-api.de/api/interpreter"
    )

    OVERPASS_TIMEOUT = 30

    # =====================================================
    # SerpAPI Configuration
    # =====================================================

    SERPAPI_BASE_URL = (
        "https://serpapi.com/search.json"
    )

    SERPAPI_TIMEOUT = 15

    # =====================================================
    # Travel Planner Configuration
    # =====================================================

    DEFAULT_START_TIME = "09:00"

    DEFAULT_END_TIME = "18:00"

    DEFAULT_MAX_POIS = 6

    DEFAULT_RADIUS_M = 15000

    AVG_VISIT_MINUTES = 60

    RESTAURANT_VISIT_MINUTES = 45

    # =====================================================
    # Distance & Travel Constants
    # =====================================================

    WALK_SPEED_M_PER_MIN = 83.33

    DRIVE_SPEED_M_PER_MIN = 666.6

    EARTH_RADIUS_M = 6371000.0

    # =====================================================
    # CORS Configuration
    # =====================================================

    CORS_HEADERS = "Content-Type"

    # =====================================================
    # Security Configuration
    # =====================================================

    JSON_SORT_KEYS = False

    JSONIFY_PRETTYPRINT_REGULAR = True

    # =====================================================
    # Environment Type
    # =====================================================

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )