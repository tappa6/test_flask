from flask import Flask
import os
import subprocess
import datetime

app = Flask(__name__)

@app.route('/htop')
def htop():
    full_name = "Your Full Name"  # Replace with your name
    username = os.getlogin()
    
    # Get server time in IST
    ist_time = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    server_time = ist_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # Get top command output
    top_output = subprocess.getoutput("top -b -n 1")

    response = f"""
    <pre>
    Name - {full_name}
    Username - {username}
    Server Time (IST): {server_time}
    
    TOP output:
    {top_output}
    </pre>
    """
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
