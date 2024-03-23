from flask import Flask, request, render_template

app = Flask(__name__)

def evaluate_expression(expression):
    try:
        result = str(eval(expression))
        return result
    except Exception as e:
        return 'Error: ' + str(e)

@app.route('/')
def home():
    return render_template('calculator.html', expression='')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form.get('expression', '')

    if 'clear' in request.form:
        if request.form['clear'] == '(':
            expression += '('
        elif request.form['clear'] == ')':
            expression += ')'
        elif request.form['clear'] == '%':
            try:
                result = evaluate_expression(expression)
                expression = str(float(result) / 100)
            except Exception as e:
                expression = 'Error: ' + str(e)

        elif request.form['clear'] == 'C':
            expression = expression[:-1] 

    elif 'value' in request.form:
        # Replace "×" with "*" and "÷" with "/"
        if expression.endswith("×") and request.form['value'] in "+-*/":
            expression = expression[:-1] + "*" + request.form['value']
        elif expression.endswith("÷") and request.form['value'] in "+-*/":
            expression = expression[:-1] + "/" + request.form['value']
        else:
            expression += request.form['value']

    elif 'calculate' in request.form:
        try:
            # Replace "×" with "*" and "÷" with "/"
            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")

            result = evaluate_expression(expression)
            expression = result
        except Exception as e:
            expression = 'Error: ' + str(e)

    return render_template('calculator.html', expression=expression)


if __name__ == '__main__':
    app.run(debug=True)
