# Description: This file contains the settings for the application
# Set all the configurations
from fastapi.middleware.cors import CORSMiddleware

SLACK_TOKEN = ""
SQLALCHEMY_DATABASE_URL = ""


# CORS configuration
CORS_CONFIG = {
    "allow_origins": ["http://127.0.0.1:5500"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_CONFIG["allow_origins"],
        allow_credentials=CORS_CONFIG["allow_credentials"],
        allow_methods=CORS_CONFIG["allow_methods"],
        allow_headers=CORS_CONFIG["allow_headers"],
    )
