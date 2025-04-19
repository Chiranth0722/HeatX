from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Serve index.html directly
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Serve CSS and JS files from root
@app.route('/<path:filename>')
def serve_static_from_root(filename):
    return send_from_directory('.', filename)

# Route for /compare
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    result = ""
    code1 = ""
    code2 = ""
    if request.method == 'POST':
        code1 = request.form.get("code1", "")
        code2 = request.form.get("code2", "")
        if len(code1) > len(code2):
            result = "Code 1 seems more optimized 🌱"
        elif len(code2) > len(code1):
            result = "Code 2 seems more optimized 🌱"
        else:
            result = "Both codes are similar in length."

    return render_template("code_comparison.html", result=result, code1=code1, code2=code2)

if __name__ == '__main__':
    app.run(debug=True)
