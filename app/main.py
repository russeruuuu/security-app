"""
Secure Flask microservice with proper input validation and error handling.
Demonstrates security best practices for API development.
"""

import logging
import os
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)

# Enable CORS with restricted origins (should be configured per environment)
CORS(app, resources={r"/api/*": {"origins": os.getenv("ALLOWED_ORIGINS", "localhost:3000")}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
MAX_INPUT_LENGTH = 255
ALLOWED_METHODS = ["GET", "POST"]


def validate_content_type(f):
    """Decorator to validate Content-Type header."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            if not request.is_json:
                logger.warning("Invalid Content-Type received")
                return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_input_length(max_length=MAX_INPUT_LENGTH):
    """Decorator to validate input string length."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "POST" and request.is_json:
                data = request.get_json()
                for key, value in data.items():
                    if isinstance(value, str) and len(value) > max_length:
                        logger.warning(f"Input length exceeded for field: {key}")
                        return jsonify({"error": f"Input exceeds maximum length of {max_length}"}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "service": "secure-app"}), 200


@app.route("/api/greet", methods=["POST"])
@validate_content_type
@validate_input_length(max_length=100)
def greet():
    """Greet endpoint with input validation."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or "name" not in data:
            logger.warning("Missing 'name' field in request")
            return jsonify({"error": "Missing required field: 'name'"}), 400
        
        name = data.get("name", "").strip()
        
        # Validate name is not empty after stripping
        if not name:
            logger.warning("Empty name provided")
            return jsonify({"error": "Name cannot be empty"}), 400
        
        # Validate name contains only safe characters
        if not all(c.isalnum() or c.isspace() or c in "-'" for c in name):
            logger.warning(f"Invalid characters in name: {name}")
            return jsonify({"error": "Name contains invalid characters"}), 400
        
        greeting = f"Hello, {name}!"
        logger.info(f"Greeting generated for: {name}")
        
        return jsonify({"message": greeting}), 200
    
    except Exception as e:
        logger.error(f"Unexpected error in greet endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/echo", methods=["POST"])
@validate_content_type
@validate_input_length(max_length=500)
def echo():
    """Echo endpoint with sanitization."""
    try:
        data = request.get_json()
        
        if not data or "text" not in data:
            logger.warning("Missing 'text' field in request")
            return jsonify({"error": "Missing required field: 'text'"}), 400
        
        text = data.get("text", "").strip()
        
        if not text:
            logger.warning("Empty text provided")
            return jsonify({"error": "Text cannot be empty"}), 400
        
        logger.info("Echo generated")
        return jsonify({"echo": text}), 200
    
    except Exception as e:
        logger.error(f"Unexpected error in echo endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Only run in development; use proper WSGI server (gunicorn) in production
    app.run(host="0.0.0.0", port=5000, debug=False)
