from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import pandas as pd
from PIL import Image
import google.generativeai as genai
import base64
import io
from werkzeug.utils import secure_filename
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', '6413749eb506f8d52efaa8523dfa6594e5fd77cecf286d42548fd92727db4630')  # Change this to a secure secret key

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Removed 'bmp' as it's not supported by Gemini
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Create upload folder if it doesn't existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the medicine dataset
def load_medicine_data():
    try:
        df = pd.read_csv('Medicine_Details.csv')
        print(f"✅ Loaded {len(df)} medicines from database")
        return df
    except Exception as e:
        print(f"❌ Error loading medicine data: {e}")
        return None

# Initialize Gemini API
def initialize_gemini():
    try:
        # You can set your API key as an environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            vision_model = genai.GenerativeModel('gemini-2.5-pro')
            text_model = genai.GenerativeModel('gemini-2.5-pro')
            print("✅ Gemini AI models initialized successfully")
            return vision_model, text_model
        else:
            print("⚠️ GOOGLE_API_KEY environment variable not set")
            return None, None
    except Exception as e:
        print(f"❌ Error initializing Gemini: {e}")
        return None, None

# Initialize models
vision_model, text_model = initialize_gemini()
medicine_df = load_medicine_data()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_medicine_name_from_image(image_path):
    if not vision_model:
        return "Error: Gemini vision model not initialized."
    try:
        # Open and convert image to RGB format (removes alpha channel and ensures compatibility)
        image = Image.open(image_path)
        
        # Convert to RGB if it's not already (handles RGBA, CMYK, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to JPEG format in memory to ensure compatibility with Gemini
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        
        # Create a new PIL Image from the converted bytes
        converted_image = Image.open(img_byte_arr)
        
        prompt = "Extract only the medicine name from this image. Return just the name, nothing else."
        response = vision_model.generate_content([prompt, converted_image])
        return response.text.strip()
    except Exception as e:
        return f"Error extracting medicine name: {e}"

def get_medicine_info_from_dataset(medicine_name):
    if medicine_df is None:
        return None
    
    # Search for medicine in the dataset (case-insensitive)
    medicine_name_lower = medicine_name.lower()
    for index, row in medicine_df.iterrows():
        if medicine_name_lower in row['Medicine Name'].lower():
            return {
                'name': row['Medicine Name'],
                'uses': row['Uses'],
                'side_effects': row['Side_effects'],
                'precautions': row.get('Precautions', 'Not available'),
                'dosage': row.get('Dosage', 'Not available')
            }
    return None

def get_gemini_description(medicine_name):
    if not text_model:
        return "Error: Gemini text model not initialized."
    try:
        prompt = f"""
Give detailed multilingual information for '{medicine_name}' in this format:

**English:**
- Uses: [Medical uses]
- Side Effects: [Common side effects]
- Precautions: [Important precautions]

**Hindi:**
- उपयोग: [Medical uses in Hindi]
- दुष्प्रभाव: [Side effects in Hindi]
- सावधानियां: [Precautions in Hindi]

**Marathi:**
- वापर: [Medical uses in Marathi]
- दुष्परिणाम: [Side effects in Marathi]
- काळजी: [Precautions in Marathi]

Keep it medical, accurate, and concise.
"""
        response = text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting medicine description: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract medicine name from image
            medicine_name = extract_medicine_name_from_image(filepath)
            
            if medicine_name.startswith('Error'):
                return jsonify({'error': medicine_name}), 500
            
            # Get information from dataset first
            dataset_info = get_medicine_info_from_dataset(medicine_name)
            
            # Get additional information from Gemini
            gemini_info = get_gemini_description(medicine_name)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({
                'medicine_name': medicine_name,
                'dataset_info': dataset_info,
                'gemini_info': gemini_info
            })
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, or GIF files.'}), 400

@app.route('/search', methods=['POST'])
def search_medicine():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        medicine_name = data.get('medicine_name', '').strip()
        
        if not medicine_name:
            return jsonify({'error': 'Medicine name is required'}), 400
        
        # Get information from dataset first
        dataset_info = get_medicine_info_from_dataset(medicine_name)
        
        # Get additional information from Gemini
        gemini_info = get_gemini_description(medicine_name)
        
        return jsonify({
            'medicine_name': medicine_name,
            'dataset_info': dataset_info,
            'gemini_info': gemini_info
        })
    except Exception as e:
        return jsonify({'error': f'Error processing search: {str(e)}'}), 500

@app.route('/api/medicines')
def get_medicines():
    if medicine_df is None:
        return jsonify({'error': 'Medicine database not available'}), 500
    
    try:
        # Return list of all medicines for autocomplete
        medicines = medicine_df['Medicine Name'].tolist()
        return jsonify({'medicines': medicines})
    except Exception as e:
        return jsonify({'error': f'Error retrieving medicines: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    print("🚀 Starting MedDetect Flask Application...")
    print(f"📊 Medicine database: {'✅ Loaded' if medicine_df is not None else '❌ Not available'}")
    print(f"🤖 Gemini AI: {'✅ Initialized' if vision_model and text_model else '❌ Not available'}")
    print("🌐 Server starting at http://localhost:5000")
    app.run() 