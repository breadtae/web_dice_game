import pandas as pd
from flask import Flask, render_template, redirect, url_for, \
    request, flash, session

import random
import re
from score_board import (load_db, save_db, add_score, gen_html)


app = Flask(__name__)
app.secret_key = "AA"
app.debug = True
html_text = re.compile(r'^"(.*)"$')


def reset_session():
    session.clear()
    session['re_user_name'] = False
    session['play_num'] = 0
    session['dice_num'] = []
    session['dice_sum'] = 0
    session['user_name'] = 'default'
    print("[Cleared Session]")


def login_required():
    pass



@app.route('/', methods=['GET', 'POST'])
def home():
    """
    1. Shows introduction message of dice game.
    2. Can select number of turns to play dice. (1/2/3)
    3. If 'play' button is pressed, redirect to play_game.html
    :return:
    """
    reset_session()
    if request.method == 'POST':
        if 'play_game' in request.form:  # Select play_num from web
            play_num = request.form.get('play_num', 'None')
            print(f"[play_num] {play_num}, [Type] {type(play_num)}")
            if play_num in ['1', '2', '3']:
                play_num = int(play_num)
                session['play_num'] = play_num  # Register play_num in session
                print(f"[Session] : {session}")
                return redirect(url_for('start_game', play_num=play_num))
            else:
                flash("[ERROR] Select valid 'Play num' !")

    return render_template('index.html')


@app.route('/start_game/<play_num>', methods=['GET', 'POST'])
def start_game(play_num):
    # TODO Require Login for future token charge system
    # login_required()
    # if session['user_name'] == 'default':
    #     return redirect(url_for('home'))

    print("redirected to /start_game")
    dice_num = []
    play_num = int(play_num)

    for num in range(play_num):
        rand_num = random.randint(1, 6)
        dice_num.append(rand_num)
    # Sum randomly generated numbers
    dice_sum = sum(dice_num)

    if session['dice_sum'] == 0:  # if initial value (Triggers only once)
        print(f"Saved dice values into session: {dice_num}, {dice_sum}")
        session['dice_num'] = dice_num
        session['dice_sum'] = dice_sum

    if request.method == 'POST':
        if 'submit_name' in request.form:
            u_name = request.form.get('user_name', None)

            if not u_name:
                print("User name is empty !")
                flash("[ERROR] Type in valid 'User Name' !")
                return render_template('play_game.html', plays=session['play_num'],
                                       dice_num=session['dice_num'],
                                       sum=session['dice_sum'])
            else:
                print(f"[USER NAME] {u_name}")
                return redirect(url_for('score_board', user_name=u_name))

    return render_template('play_game.html', plays=play_num, dice_num=dice_num, sum=dice_sum)


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
    print(f"[Session] {session}")
    print(f"redirected to /score_board/{user_name}")

    # Generate DB and show DB
    score_data = load_db()
    html_df = None

    if score := session['dice_sum']:
        # TODO Think about case of user_name is None (w/o playing game)
        score_data = add_score(score_data, user_name.upper().strip(), score)
        save_db(score_data)
        # Change dataframe into HTML Table
        html_df = gen_html(score_data)
    else: # Direct access from index.html
        pass

    return render_template('score_board.html', user_name=user_name, score=session['dice_sum'], html_df=html_df)


if __name__ == '__main__':
    print(f"Running {__name__} server")
    app.run(host='0.0.0.0', port=50003)
