from flask import Flask, render_template, redirect, url_for, \
    request, flash, session

import random
from flask import jsonify

import logging

app = Flask(__name__)
app.secret_key = "AA"
app.debug = True


def reset_session():
    session.clear()
    print("[Clear Session]")

# Home page to show Game Entry
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    1. Shows introduction message of dice game.
    2. Can select number of turns to play dice. (1/2/3)
    3. If 'play' button is pressed, redirect to play_game.html
    :return:
    """
    reset_session()
    flash(f"[Session] {session}")

    if request.method == 'POST':
        if 'play_game' in request.form:  # Select play_num from web
            play_num = request.form.get('play_num')
            session['play_num'] = play_num
            print(f"[RECEIVED] Play_num : {play_num}")
            return redirect(url_for('start_game', play_num=play_num))

    return render_template('index.html')


@app.route('/start_game/<play_num>', methods=['GET', 'POST'])
def start_game(play_num):
    flash(f"[Session] {session}")
    print("redirected to /start_game")

    dice_num = []

    play_num = int(play_num)
    for num in range(play_num):
        rand_num = random.randint(1, 6)
        dice_num.append(rand_num)
    # Sum randomly generated numbers
    dice_sum = sum(dice_num)

    session['dice_num'] = dice_num
    session['dice_sum'] = dice_sum

    if request.method == 'POST':
        if 'submit_name' in request.form:
            u_name = request.form.get('user_name', None)
            print(f"[USER NAME] {u_name}")

            # TODO Write data in Database
            if not u_name:
                print("User name is empty !")
                return redirect()
            else:
                return redirect(url_for('score_board', user_name=u_name))

    return render_template('play_game.html', plays=play_num, dice_num=dice_num, sum=dice_sum)


# TODO
def write_db(user_name:str, score:int):
    pass


@app.route('/score_board/<user_name>', methods=['GET'])
def score_board(user_name=None):
    """
    Shows score board of players
    - Highlights user_name when render_template
    - Reset every 30 min

    Render Table from json database

    :param user_name: Name received from user in play_game.html
    :return:
    """
    flash(f"[Session] {session}")
    print(f"redirected to /score_board/{user_name}")
    return render_template('score_board.html', user_name=user_name)


if __name__ == '__main__':
    print(f"Running {__name__} server")
    app.run(host='0.0.0.0', port=50003)
