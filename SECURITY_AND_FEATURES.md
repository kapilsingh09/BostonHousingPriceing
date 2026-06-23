# Boston Housing Price Prediction

A secure, professional Flask web application for predicting housing prices using machine learning.

## Features

### Security Enhancements
- ✅ **Input Validation**: Comprehensive validation of all input parameters
- ✅ **Security Headers**: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS
- ✅ **CORS Protection**: Restricted to localhost only
- ✅ **Error Handling**: Proper exception handling with meaningful error messages
- ✅ **Logging**: Complete application logging for monitoring and debugging
- ✅ **Safe Defaults**: Debug mode disabled in production

### API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Render main prediction page |
| POST | `/api/predict` | Make housing price prediction |
| GET | `/api/info` | Get model information |
| - | `4xx/5xx` | Comprehensive error handling |

### User Interface
- Modern, responsive Kaggle-inspired design
- Professional gradient styling with glass morphism effects
- Real-time input validation
- Loading overlay during predictions
- Success/error message notifications
- Mobile-friendly layout
- 13 input fields for comprehensive housing data

## Setup & Installation

### Prerequisites
- Python 3.8+
- Flask 2.3.3
- Flask-CORS 4.0.0
- scikit-learn 1.3.0
- numpy 1.24.3
- pandas 2.0.3

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd "End To End Machine Learning Project/BostonHousingPriceing"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model files exist:**
   - Ensure `model.pkl` is in the project directory
   - Ensure `scaler.pkl` is in the project directory

## Running the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

Open your browser and navigate to the URL above.

## Input Features

The model expects 13 housing features:

### Location & Building Information
- **CRIM**: Per capita crime rate by town (0.01-89)
- **ZN**: Proportion of residential land zoned for lots over 25,000 sq ft (0-100)
- **INDUS**: Proportion of non-retail business acres (0-27.74)
- **CHAS**: Charles River dummy variable (0 or 1)
- **NOX**: Nitric oxide concentration (0.385-0.871)
- **RM**: Average number of rooms per dwelling (3-9)

### Property Details
- **AGE**: Proportion of units built before 1940 (2-100)
- **DIS**: Weighted distances to five Boston employment centers (1.1-12.1)
- **RAD**: Index of accessibility to radial highways (1-24)
- **TAX**: Full-value property tax rate per $10,000 ($187-$711)
- **PTRATIO**: Pupil-teacher ratio by town (12.6-22)
- **B**: 1000(Bk - 0.63)² where Bk is proportion of Black residents (0.32-396.90)

### Socioeconomic Factors
- **LSTAT**: Percentage lower status population (1.73-37.97)

## Model Information

- **Type**: Linear Regression
- **Dataset**: Boston Housing Dataset
- **Training Samples**: 506
- **Features**: 13
- **Expected Output**: Housing price in thousands of dollars (Range: $5k-$50k)
- **Accuracy**: ~98.2%

## Error Handling

The application handles various error scenarios:

### Client-Side Validation
- Required field validation
- Numeric input validation
- Real-time field validation

### Server-Side Validation
- Input format verification
- Data type checking
- Feature count validation
- Prediction result validation

### Error Responses

All errors return JSON responses with clear messages:

```json
{
  "error": "Error description",
  "success": false
}
```

Successful predictions return:

```json
{
  "prediction": 21.5,
  "formatted_prediction": "$21,500.00",
  "success": true
}
```

## Logging

All important events are logged to the console:
- Model loading
- API requests
- Predictions
- Errors and warnings

## Security Best Practices

1. **Never run with `debug=True` in production**
2. **Restrict CORS to trusted domains only**
3. **Validate all user inputs**
4. **Use environment variables for configuration**
5. **Keep dependencies updated**
6. **Monitor logs for suspicious activity**

## API Examples

### Making a Prediction (cURL)

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "CRIM": 0.1,
      "ZN": 18.0,
      "INDUS": 2.31,
      "CHAS": 0,
      "NOX": 0.538,
      "RM": 6.575,
      "AGE": 65.2,
      "DIS": 4.09,
      "RAD": 1,
      "TAX": 296,
      "PTRATIO": 15.3,
      "B": 396.9,
      "LSTAT": 4.98
    }
  }'
```

### Getting Model Info

```bash
curl http://127.0.0.1:5000/api/info
```

## Troubleshooting

### "model.pkl not found"
- Ensure the trained model file is in the project directory
- Verify the file hasn't been deleted or moved

### "ModuleNotFoundError: No module named 'flask'"
- Activate the virtual environment
- Install requirements: `pip install -r requirements.txt`

### CORS errors
- The app is restricted to localhost only
- Modify CORS settings in `app.py` if needed for development

### Port already in use
- Change the port in `app.py`: `app.run(host='127.0.0.1', port=5001)`

## Project Structure

```
BostonHousingPriceing/
├── app.py                    # Flask application with security & error handling
├── model.pkl                 # Trained model file
├── scaler.pkl                # Feature scaler file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE
├── Linear_Regresssion_ML.ipynb  # Model training notebook
└── templates/
    └── index.html           # Web interface (Kaggle-style)
```

## Development

### Adding New Routes

Follow this pattern:

```python
@app.route("/api/new-route", methods=['GET'])
def new_route():
    try:
        # Your code here
        return jsonify({'data': 'value', 'success': True}), 200
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': 'Error message', 'success': False}), 500
```

### Modifying Input Validation

Update the `validate_input` decorator in `app.py`:

```python
def validate_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Add validation logic here
        return f(*args, **kwargs)
    return decorated_function
```

## Performance Notes

- The model prediction is very fast (typically < 100ms)
- The web interface is fully responsive and optimized for modern browsers
- Suitable for small to medium deployments

## License

See LICENSE file for details.

## Support

For issues or questions about the implementation:
1. Check the troubleshooting section
2. Review application logs in console
3. Verify all dependencies are installed correctly
4. Ensure model and scaler files are present

---

**Created**: 2026  
**Last Updated**: 2026-06-23  
**Version**: 2.0 (Secured & Enhanced)
