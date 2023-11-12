from flask import Flask, render_template, redirect, url_for
from flask import jsonify


app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('index.html')

@app.route('/start_game', methods=['GET', 'POST'])
def start_game():

    return render_template('play_game.html')


if __name__ == '__main__':
    print(f"Running {__name__} server")
    app.run()
