from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def last_lines():
    filename = 'data.txt'
    n = 10  # Number of last lines to display
    
    try:
        with open(filename, 'r') as f:
            # Read all lines and take the last n
            lines = f.readlines()[-n:]
    except FileNotFoundError:
        lines = ['File not found']

    # Pass lines to template
    return render_template('last_lines.html', lines=lines)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
