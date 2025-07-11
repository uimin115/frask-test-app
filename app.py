from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import os
import datetime
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('test', username=username))
    return render_template('index.html')

@app.route('/test/<username>', methods=['GET'])
def test(username):
    return render_template('test.html', username=username)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    username = data['username']
    entries = data['results']

    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results_{now}_{username}.csv"
    filepath = os.path.join("results", filename)

    os.makedirs("results", exist_ok=True)

    with open(filepath, 'w', newline='', encoding='euc-kr') as f:
        writer = csv.DictWriter(f, fieldnames=["types", "problems", "correction", "answers", "T or F", "time(s)"])
        writer.writeheader()
        for row in entries:
            writer.writerow(row)

    return {"filename": filename}

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join("results", filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
