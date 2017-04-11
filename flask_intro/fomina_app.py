from flask import Flask
from flask import render_template, request

app = Flask(__name__)

stats = {}
all_names = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    global stats
    global all_names
    if request.args:
        name = request.args['name']
        animal = request.args['animal']

        if name not in all_names:
            all_names[name] = 1
        else:
            all_names[name] +=1
            
        if animal not in stats:
            stats[animal] = 1
        else:
            stats[animal] +=1

    return render_template('result.html', stats = stats, all_names = all_names)

if __name__ == '__main__':
    app.run(debug=True)
