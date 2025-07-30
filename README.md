# 🏥 MedDetect - Comprehensive Medicine Detection & Analysis System

A sophisticated Flask web application that combines multiple AI/ML approaches for medicine detection, analysis, and prediction. The system features OCR capabilities, deep learning models, traditional machine learning models, and a modern web interface.

## 🌟 Key Features

### 🔍 **Multi-Modal Detection**
- **Image Upload & OCR**: Extract medicine names from pill images
- **Text Input**: Direct medicine name search
- **Real-time Processing**: Instant results with confidence scores

### 🤖 **Advanced AI Models**
- **Deep Learning (LSTM)**: Neural network-based medicine prediction
- **Machine Learning (RF/SVM)**: Traditional ML approach with ensemble methods
- **Model Comparison**: Comprehensive evaluation and benchmarking
- **Confidence Scoring**: Reliability metrics for predictions

### 💊 **Comprehensive Medicine Information**
- **Uses & Indications**: Detailed therapeutic applications
- **Side Effects**: Complete adverse reaction profiles
- **Drug Interactions**: Potential medication conflicts
- **Dosage Information**: Recommended usage guidelines

### 🎨 **Modern Web Interface**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Search**: Instant suggestions and autocomplete
- **Interactive Results**: Expandable information cards
- **Dark/Light Theme**: User preference support

## 📁 Project Structure

```
Medicine Detection/
├── app.py                          # Main Flask application
├── run.py                          # Startup script with environment checks
├── requirements.txt                # Python dependencies
├── SETUP.md                        # Detailed setup instructions
├── README.md                       # This comprehensive guide
├── 
├── models/                         # AI/ML Models
│   ├── medicine_model.py           # Deep Learning (LSTM) model
│   ├── medicine_ml_model.py        # Traditional ML (RF/SVM) model
│   └── model_evaluation.py         # Model comparison & evaluation
│
├── utils/                          # Utility Functions
│   ├── ocr.py                      # OCR functionality for image processing
│   └── database.py                 # Medicine database operations
│
├── static/                         # Web Assets
│   ├── css/
│   │   ├── style.css              # Main stylesheet
│   │   └── dark-theme.css         # Dark theme styles
│   ├── js/
│   │   ├── script.js              # Main JavaScript
│   │   └── search.js              # Search functionality
│   └── images/                    # UI images and icons
│
├── templates/                      # HTML Templates
│   ├── index.html                 # Main application page
│   ├── base.html                  # Base template
│   └── components/                # Reusable components
│
└── data/                          # Data Files
    ├── medicines.csv              # Medicine database
    └── sample_images/             # Test images for OCR
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Medicine-Detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Access the application**
   - Open your browser
   - Navigate to `http://localhost:5000`
   - Start detecting medicines!

## 🧠 AI/ML Models

### Deep Learning Model (`medicine_model.py`)
- **Architecture**: LSTM with Attention Mechanism
- **Features**: 
  - Sequence learning for medicine names
  - Attention weights for interpretability
  - Confidence scoring
  - Batch processing capabilities
- **Usage**: `python medicine_model.py`

### Machine Learning Model (`medicine_ml_model.py`)
- **Algorithms**: Random Forest + Support Vector Machine
- **Features**:
  - Ensemble learning approach
  - Hyperparameter tuning
  - Cross-validation
  - Feature importance analysis
- **Usage**: `python medicine_ml_model.py`

### Model Evaluation (`model_evaluation.py`)
- **Comprehensive Comparison**: Success rates, response times, confidence scores
- **Visualization**: Charts and graphs for model performance
- **Detailed Reports**: Text and visual analysis
- **Usage**: `python model_evaluation.py`

## 🔧 OCR Functionality (`ocr.py`)

### Features
- **Image Preprocessing**: Noise reduction, contrast enhancement
- **Text Extraction**: Using Tesseract OCR engine
- **Medicine Name Recognition**: Pattern matching and validation
- **Database Integration**: Automatic lookup after extraction

### Usage
```python
from ocr import OCRProcessor

processor = OCRProcessor()
result = processor.extract_medicine_name('path/to/image.jpg')
print(f"Detected medicine: {result}")
```

## 📊 Database Structure

The system uses a CSV-based medicine database with the following structure:

| Column | Description |
|--------|-------------|
| `name` | Medicine name |
| `uses` | Therapeutic uses and indications |
| `side_effects` | Adverse reactions and side effects |
| `interactions` | Drug interactions |
| `dosage` | Recommended dosage information |

## 🎯 API Endpoints

### Main Routes
- `GET /` - Main application interface
- `POST /search` - Medicine search endpoint
- `POST /upload` - Image upload and OCR processing
- `GET /api/medicines` - JSON API for medicine data

### Response Format
```json
{
  "success": true,
  "medicine": {
    "name": "Paracetamol",
    "uses": "Pain relief, fever reduction",
    "side_effects": "Nausea, liver problems",
    "confidence": 0.95
  }
}
```

## 🛠️ Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' for debug mode
- `SECRET_KEY`: Flask secret key for sessions
- `UPLOAD_FOLDER`: Directory for uploaded images

### Customization
- **Database**: Replace `data/medicines.csv` with your own data
- **Models**: Modify model parameters in respective files
- **UI**: Customize styles in `static/css/`
- **OCR**: Adjust preprocessing parameters in `ocr.py`

## 📈 Performance Metrics

### Model Performance
- **Success Rate**: Percentage of successful predictions
- **Response Time**: Average processing time per request
- **Confidence Score**: Reliability of predictions (0-1)
- **Accuracy**: Model prediction accuracy

### System Performance
- **Concurrent Users**: Supports multiple simultaneous users
- **Image Processing**: Fast OCR with preprocessing
- **Memory Usage**: Optimized for efficient resource usage

## 🔒 Security Features

- **Input Validation**: Sanitized user inputs
- **File Upload Security**: Restricted file types and sizes
- **Error Handling**: Graceful error management
- **Session Management**: Secure user sessions

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **OCR Not Working**
   - Install Tesseract OCR: `sudo apt-get install tesseract-ocr`
   - Windows: Download from GitHub releases

3. **Model Loading Errors**
   - Train models first: `python medicine_model.py`
   - Check file permissions

4. **Port Already in Use**
   ```bash
   python run.py --port 5001
   ```

### Debug Mode
```bash
export FLASK_ENV=development
python run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Flask**: Web framework
- **TensorFlow**: Deep learning capabilities
- **Scikit-learn**: Machine learning algorithms
- **Tesseract**: OCR functionality
- **Bootstrap**: UI components

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the SETUP.md file

## 🔄 Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Added deep learning model
- **v1.2.0**: Added machine learning model
- **v1.3.0**: Added OCR functionality
- **v1.4.0**: Added model evaluation system
- **v1.5.0**: Enhanced UI and performance

---

**Made with ❤️ for better healthcare through AI** 