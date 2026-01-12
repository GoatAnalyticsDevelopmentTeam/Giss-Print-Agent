import os
import sys
import base64
import tempfile
import subprocess
import json
import threading
import hmac
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    import win32print
except ImportError:
    win32print = None

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None

app = Flask(__name__)
CORS(app)

# 10 MB Limit
MAX_PDF_SIZE = 10 * 1024 * 1024

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """
    Config dosyasını yükler. 
    Dosya yoksa veya api_key eksikse None döner.
    Varsayılan şifre veya dosya oluşturma YOK.
    """
    config_path = os.path.join(get_base_path(), "config.json")
    
    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, 'r') as f:
            data = json.load(f) 
            if "api_key" not in data or not data["api_key"]:
                return None
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Config load error: {e}")
        return None
 
config = load_config()
 
if config is None:
    print("ERROR: config.json not found or invalid (api_key missing)!")
    sys.exit(1) 

@app.before_request
def check_api_key():
    if request.method == 'OPTIONS':
        return None
    api_key = request.headers.get('X-Api-Key') 
    if not api_key or not hmac.compare_digest(api_key, config.get('api_key')):
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
        decoded_pdf = base64.b64decode(pdf_base64)
        if len(decoded_pdf) > MAX_PDF_SIZE:
            return jsonify({"error": "PDF file too large (max 10MB)"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(decoded_pdf)
            temp_file_path = temp_pdf.name
        command = [sumatra_path, "-print-to", printer_name, "-silent", temp_file_path] 
        subprocess.run(command, check=True, timeout=30)
        return jsonify({"message": "Print job sent successfully"}), 200
    except subprocess.TimeoutExpired:
        return jsonify({"error": "SumatraPDF execution timed out"}), 500
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

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_icon_image():
    icon_path = get_resource_path(os.path.join("src", "icon.png"))
    if os.path.exists(icon_path):
        try:
            return Image.open(icon_path)
        except Exception as e:
            print(f"Error loading icon: {e}")
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill=color2)
    return image

def on_quit(icon, item):
    icon.stop()
    os._exit(0)

def run_server(): 
    host_val = config.get('host', '127.0.0.1')
    port_val = config.get('port', 5000)
    app.run(host=host_val, port=port_val, debug=False, use_reloader=False)

if __name__ == '__main__':
    if pystray:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        icon = pystray.Icon("GissPrintAgent", get_icon_image(), "Giss Print Agent", menu=pystray.Menu(
            pystray.MenuItem("Quit", on_quit)
        ))
        icon.run()
    else: 
        host_val = config.get('host', '127.0.0.1')
        port_val = config.get('port', 5000)
        app.run(host=host_val, port=port_val, debug=False)