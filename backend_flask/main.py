from flask import Flask, render_template, request, jsonify
import hashlib 
import json
import os

app = Flask(__name__)

ADMIN_PW = "4097889236a2af26c293033feb964c4cf118c0224e0d063fec0a89e9d0569ef2"
scores = {
    'toges': 0,
    'non-toges': 0,
}
SCORES_FILE = 'scores.json'

def save_scores():
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def load_scores():
    global scores
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)

@app.route('/')
def hello_world():
   return """
        <p>Hello from the Rasb 🍓 !<p>
        <p><a href="/cli">Link<a> to the cli page</p>
        <p><a href="/change_display">Link<a> to the change_display page</p>
        """

@app.route('/cli', methods=['GET', 'POST'])
def cli():
    if request.method == 'POST':
        pw = request.form.get('pw')  
        pw_hashed = hashlib.sha256(pw.encode()).hexdigest() 
        if pw_hashed == ADMIN_PW:
            return render_template('/enfer/admin.html')
        else:
            return render_template('/enfer/login.html', wrongPassword = True, sha256 = pw_hashed)
    else:
        return render_template('/enfer/login.html')

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.get_json()
        operation = data.get('operation')
        cercle = data.get('cercle')

        if operation == 'add':
            scores[cercle] += 1
        elif operation == 'sub' and scores[cercle] > 0:
            scores[cercle] -= 1
        save_scores()
        return jsonify({'succeed': True, 'scores': scores})
    else:
        return jsonify(scores) 

@app.route('/display')
def display():
    return render_template('/enfer/display.html')


@app.route('/change_display')
def change_display():
    return render_template('/change_display/index.html')

@app.route('/change_display_api', methods=['GET', 'POST'])
def change_display_api():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('operation') == 'enfer':
            os.system('firefox http://127.0.0.1:5000/display')


if __name__ == '__main__':
    load_scores()
    app.run(debug=True)
    save_scores()