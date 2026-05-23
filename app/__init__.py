from flask import Flask
from flask_cors import CORS
import logging

from config import Config

# =====================================================
# Application Factory
# =====================================================

def create_app():

    app = Flask(
        __name__,
        static_folder=Config.STATIC_FOLDER,
        template_folder=Config.TEMPLATE_FOLDER
    )

    # =================================================
    # Load Configuration
    # =================================================

    app.config.from_object(Config)

    # =================================================
    # Secret Key
    # =================================================

    app.secret_key = app.config["SECRET_KEY"]

    # =================================================
    # Enable CORS
    # =================================================

    CORS(
    app,
    supports_credentials=True
)

    # =================================================
    # Initialize Database
    # =================================================

   

    # =================================================
    # Logging Configuration
    # =================================================

    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format=Config.LOG_FORMAT
    )

    logger = logging.getLogger("main_app")

    logger.info("Application initialized successfully")

    # =================================================
    # Register Blueprints
    # =================================================

    from app.routes.auth_routes import auth_bp
    from app.routes.trip_routes import trip_bp
    from app.routes.weather_routes import weather_bp
    from app.routes.hotel_routes import hotel_bp
    from app.routes.review_routes import review_bp
    from app.routes.routefinder_routes import routefinder_bp
    from app.routes.schedule_routes import schedule_bp
    from app.routes.suggestion_routes import suggestion_bp
    from app.routes.findmyway_routes import findmyway_bp
    from app.routes.location_routes import location_bp
   

    app.register_blueprint(auth_bp)

    app.register_blueprint(trip_bp)

    app.register_blueprint(weather_bp)

    app.register_blueprint(hotel_bp)

    app.register_blueprint(review_bp)

    app.register_blueprint(routefinder_bp)

    app.register_blueprint(schedule_bp)

    app.register_blueprint(suggestion_bp)

    app.register_blueprint(findmyway_bp)

    app.register_blueprint(location_bp)

  

    

    # =================================================
    # Return Flask App
    # =================================================

    return app