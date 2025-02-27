# Ath vs Bx 
prefixAthVsBx = '/ath_vs_bx'

scores = {'Ath': 0, 'Bx': 0}

@app.route(prefixAthVsBx + '/display')
def display():
    return render_template('display_screens/ath-vs-bx.html', score_ath=scores['Ath'], score_bx=scores['Bx'])

@app.route(prefixAthVsBx + '/cli', methods=['POST', 'GET'])
def cli():
    if request.method == 'POST':
        if request.form.get('pw') == ADMIN_PW:
            return render_template('cli/ath-vs-bx/admin-panel.html', credential=ADMIN_PW)
        else:
            return render_template('cli/ath-vs-bx/login.html')
    return render_template('cli/ath-vs-bx/login.html')

@app.route(prefixAthVsBx + '/api', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        data = request.get_json()
        operation = data.get('operation')
        city = data.get('city')

        if operation == 'add':
            scores[city] += 1
        elif operation == 'subtract' and scores[city] > 0:
            scores[city] -= 1

        return jsonify({'succeed': True, 'scores': scores})

    else:
        return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True)