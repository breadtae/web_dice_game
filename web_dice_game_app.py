from flask import Flask, render_template, redirect, url_for, \
    request, flash, session

import random
from flask import jsonify

import logging

app = Flask(__name__)
app.secret_key = "AA"
app.debug = True


# Home page to show Game Entry
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    1. Shows introduction message of dice game.
    2. Can select number of turns to play dice. (1/2/3)
    3. If 'play' button is pressed, redirect to play_game.html
    :return:
    """
    flash("Content for flash message")

    if request.method == 'POST':
        play_num = request.form.get('play_num')
        print(f"[RECEIVED] Play_num : {play_num}")
        return redirect(url_for('start_game', play_num=play_num))

    return render_template('index.html')


@app.route('/start_game/<play_num>', methods=['GET', 'POST'])
def start_game(play_num):
    print("redirected to /start_game")

    dice_num = []
    play_num = int(play_num)
    for num in range(play_num):
        dice_num.append(random.randint(1, 6))

    dice_sum = sum(dice_num)

    if request.method == 'POST':
        # TODO Enable submit and redirect
        if request.form.get('submit', 'none') == 'submit':
            print(f"[RECEIVED] return")
             # Clear up session
            return redirect(url_for('home'))
        else:
            print(f"RECEIVED {request.form}")

    return render_template('play_game.html', plays=play_num, dice_num=dice_num, sum=dice_sum)


if __name__ == '__main__':
    print(f"Running {__name__} server")
    app.run()
