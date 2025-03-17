from flask import Flask
import os
import datetime
import subprocess

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Fetch system username
    username = os.getenv('USER') or os.getenv('USERNAME') or "Unknown User"
    
    # Get IST Time
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    
    # Fetch 'top' command output (limited to 10 lines for clarity)
    try:
        top_output = subprocess.check_output("top -b -n 1 | head -10", shell=True, universal_newlines=True)
    except Exception as e:
        top_output = f"Error fetching top output: {str(e)}"
    
    # HTML Response
    return f"""
    <html>
    <body>
        <h1>System Info</h1>
        <p><b>Name:</b> SHIV POOJAN PAL</p>
        <p><b>Username:</b> {username}</p>
        <p><b>Server Time (IST):</b> {ist_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <h2>Top Output:</h2>
        <pre>{top_output}</pre>
    </body>
    </html>
    """

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)