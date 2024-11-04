from flask import Flask, send_file

app = Flask(__name__)

@app.route('/generate_csv')
def generate_csv():
    return send_file('backend/calculated_data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
