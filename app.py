from flask import Flask, render_template, request
import ast

app = Flask(__name__)

def calculate_ecoscore(code):
    try:
        tree = ast.parse(code)
        functions = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
        loops = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
        lines = len(code.splitlines())
        score = 100 - (lines * 0.5 + loops * 2 - functions * 1.5)
        return max(0, min(100, score))
    except:
        return 0

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        code1 = request.form['code1']
        code2 = request.form['code2']
        score1 = calculate_ecoscore(code1)
        score2 = calculate_ecoscore(code2)

        if score1 > score2:
            result = f"Code 1 is more optimized. (EcoScore: {score1:.2f} vs {score2:.2f})"
        elif score2 > score1:
            result = f"Code 2 is more optimized. (EcoScore: {score2:.2f} vs {score1:.2f})"
        else:
            result = f"Both codes have the same EcoScore: {score1:.2f}"

        return render_template('code_comparison.html', code1=code1, code2=code2, result=result)

    return render_template('code_comparison.html', code1="", code2="", result=None)

if __name__ == '__main__':
    app.run(debug=True)
