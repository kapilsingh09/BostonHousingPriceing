import pickle
import logging
from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
from functools import wraps
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security configurations
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Add security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Load model and scaler with error handling
try:
    if not os.path.exists("model.pkl"):
        raise FileNotFoundError("model.pkl not found")
    if not os.path.exists("scaler.pkl"):
        raise FileNotFoundError("scaler.pkl not found")
    
    model = pickle.load(open("model.pkl", 'rb'))
    scaler = pickle.load(open("scaler.pkl", 'rb'))
    logger.info("Model and scaler loaded successfully")
except Exception as e:
    logger.error(f"Error loading model or scaler: {str(e)}")
    raise


def validate_input(f):
    """Decorator to validate input data"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not request.json or 'data' not in request.json:
                return jsonify({
                    'error': 'Invalid request format. Expected JSON with "data" key',
                    'success': False
                }), 400
            
            data = request.json['data']
            
            # Validate data is a dictionary
            if not isinstance(data, dict):
                return jsonify({
                    'error': 'Data must be a dictionary',
                    'success': False
                }), 400
            
            # Validate all values are numeric
            for key, value in data.items():
                try:
                    float(value)
                except (ValueError, TypeError):
                    return jsonify({
                        'error': f'Invalid value for {key}. All values must be numeric',
                        'success': False
                    }), 400
            
            # Validate we have the right number of features
            expected_features = scaler.n_features_in_
            if len(data) != expected_features:
                return jsonify({
                    'error': f'Expected {expected_features} features, got {len(data)}',
                    'success': False
                }), 400
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({
                'error': 'Validation error occurred',
                'success': False
            }), 500
    return decorated_function


@app.route('/')
def home():
    """Render home page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        return jsonify({
            'error': 'Error loading page',
            'success': False
        }), 500


@app.route("/api/predict", methods=['POST'])
@validate_input
def predict_api():
    """Make prediction based on input features"""
    try:
        data = request.json['data']
        
        # Convert data to numpy array
        input_array = np.array(list(data.values())).reshape(1, -1)
        
        # Scale the input
        scaled_data = scaler.transform(input_array)
        
        # Make prediction
        prediction = model.predict(scaled_data)[0]
        
        # Validate prediction
        if np.isnan(prediction) or np.isinf(prediction):
            raise ValueError("Invalid prediction result")
        
        logger.info(f"Prediction successful: ${prediction:.2f}")
        
        return jsonify({
            'prediction': float(prediction),
            'formatted_prediction': f"${prediction:,.2f}",
            'success': True
        }), 200
        
    except ValueError as e:
        logger.error(f"Value error in prediction: {str(e)}")
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error in prediction: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred during prediction',
            'success': False
        }), 500


@app.route("/api/info", methods=['GET'])
def info():
    """Get model information"""
    try:
        return jsonify({
            'model_type': type(model).__name__,
            'num_features': int(scaler.n_features_in_),
            'scaler_type': type(scaler).__name__,
            'success': True
        }), 200
    except Exception as e:
        logger.error(f"Error getting info: {str(e)}")
        return jsonify({
            'error': 'Error retrieving model info',
            'success': False
        }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    logger.warning(f"Bad request: {str(error)}")
    return jsonify({
        'error': 'Bad request',
        'success': False
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"Not found: {str(error)}")
    return jsonify({
        'error': 'Endpoint not found',
        'success': False
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all exceptions"""
    logger.error(f"Unhandled exception: {str(error)}")
    return jsonify({
        'error': 'An unexpected error occurred',
        'success': False
    }), 500


if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=False, host='127.0.0.1', port=5000)

