import os
import sys
import base64
import tempfile
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    import win32print
except ImportError:
    win32print = None

app = Flask(__name__)
CORS(app)

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    config_path = os.path.join(get_base_path(), "config.json")
    default_config = {"port": 5000, "api_key": "giss_secret_token"}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    return default_config

config = load_config()

@app.before_request
def check_api_key():
    api_key = request.headers.get('X-Api-Key')
    if api_key != config.get('api_key'):
        return jsonify({"error": "Unauthorized"}), 401

def get_sumatra_path():
    return os.path.join(get_base_path(), "SumatraPDF.exe")

@app.route('/printers', methods=['GET'])
def list_printers():
    if win32print is None:
        return jsonify({"error": "win32print module not found. This service must run on Windows."}), 500
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printer_names = [printer[2] for printer in printers]
        return jsonify(printer_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/print', methods=['POST'])
def print_pdf():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    printer_name = data.get('printer_name')
    pdf_base64 = data.get('pdf_data')
    if not printer_name or not pdf_base64:
        return jsonify({"error": "Missing printer_name or pdf_data"}), 400
    sumatra_path = get_sumatra_path()
    if not os.path.exists(sumatra_path):
        return jsonify({"error": f"SumatraPDF.exe not found at {sumatra_path}"}), 500
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(base64.b64decode(pdf_base64))
            temp_file_path = temp_pdf.name
        command = [sumatra_path, "-print-to", printer_name, "-silent", temp_file_path]
        subprocess.check_call(command)
        return jsonify({"message": "Print job sent successfully"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"SumatraPDF execution failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_error:
                print(f"Error deleting temp file: {cleanup_error}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get('port', 5000), debug=False)
