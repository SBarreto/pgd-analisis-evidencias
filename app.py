from flask import Flask

app = Flask(__name__)

@app.route('/analitica/evidencias')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(debug=True)