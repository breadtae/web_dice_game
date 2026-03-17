import os
import random

from flask import Flask, render_template, redirect, url_for, request, flash, session

from score_board import load_db, save_db, add_score, to_records


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.debug = True


def reset_session():
    session.clear()
    session['play_num'] = 0
    session['dice_num'] = []
    session['dice_sum'] = 0


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page: select number of dice to roll."""
    reset_session()
    if request.method == 'POST':
        if 'play_game' in request.form:
            play_num = request.form.get('play_num', '')
            if play_num in ['1', '2', '3']:
                session['play_num'] = int(play_num)
                return redirect(url_for('start_game', play_num=play_num))
            else:
                flash("주사위 개수를 선택해주세요! (1 / 2 / 3)")

    return render_template('index.html')


@app.route('/start_game/<int:play_num>', methods=['GET', 'POST'])
def start_game(play_num):
    """Roll dice and let user enter their name."""
    # Only generate new dice on first visit; preserve on refresh/re-submit
    if not session.get('dice_num'):
        dice_num = [random.randint(1, 6) for _ in range(play_num)]
        session['dice_num'] = dice_num
        session['dice_sum'] = sum(dice_num)
        session['play_num'] = play_num

    dice_num = session['dice_num']
    dice_sum = session['dice_sum']

    if request.method == 'POST' and 'submit_name' in request.form:
        u_name = request.form.get('user_name', '').strip()
        if not u_name:
            flash("유효한 이름을 입력해주세요!")
        else:
            return redirect(url_for('score_board', user_name=u_name))

    return render_template('play_game.html', plays=play_num,
                           dice_num=dice_num, dice_sum=dice_sum)


@app.route('/score_board/<user_name>', methods=['GET'])
def score_board(user_name):
    """Show rankings and highlight the current player."""
    score_data = load_db()
    score = session.get('dice_sum', 0)
    play_num = session.get('play_num', 1)
    display_name = user_name.upper().strip()

    if score:
        score_data = add_score(score_data, display_name, score, dice_count=play_num)
        save_db(score_data)

    records = to_records(score_data)
    return render_template('score_board.html',
                           user_name=display_name,
                           score=score,
                           records=records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50003)
