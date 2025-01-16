from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

def get_wifi_password():
    try:
        profiles_data = os.popen('netsh wlan show profiles').read()
        profiles = [line.split(":")[1].strip() for line in profiles_data.splitlines() if "All User Profile" in line]
        
        if not profiles:
            return {"error": "No Wi-Fi profiles found."}

        wifi_passwords = {}
        for profile in profiles:
            wifi_data = os.popen(f'netsh wlan show profile name="{profile}" key=clear').read()
            if "Key Content" in wifi_data:
                password_line = [line for line in wifi_data.splitlines() if "Key Content" in line]
                password = password_line[0].split(":")[1].strip()
                wifi_passwords[profile] = password
            else:
                wifi_passwords[profile] = "None or Encrypted"

        return wifi_passwords
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_wifi_passwords', methods=['GET'])
def get_wifi_passwords():
    result = get_wifi_password()
    return jsonify(result)

# Route to serve the HTML file
@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')  # Ensure the HTML file is in the same directory as this script

if __name__ == "__main__":
    app.run(debug=True)
