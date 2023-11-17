import pandas
import pandas as pd
import logging
import os

logger = logging.getLogger('score_board')
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('[%(levelname)s] %(funcName)s \n%(message)s\n')

file_handler = logging.FileHandler('score_board.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


"""
[Gets]
- sum of dices and each number(s)

[Stores]
- dataframe of scoreboard
     rank | name  | score |
        1 |  tae  | 18    |
        1 |  min  | 18    |
        2 |  joe  |  3    |
"""


MAX_USERS_NUM = 10
db_file_name = 'score.json'

sample_score_1 = {'name': 'tae', 'score': '18'}
sample_score_2 = {'name': 'joe', 'score': '3'}
sample_score_3 = {'name': 'joe', 'score': '4'}
sample_score_4 = {'name': 'joe', 'score': '3'}

df_data = pd.DataFrame([sample_score_1, sample_score_2, sample_score_3, sample_score_4])


def load_db():
    if os.path.exists(db_file_name):
        logger.info(f'Loaded {db_file_name}')
        return pd.read_json(db_file_name)
    else:
        logger.info('No json file to load')
        return pd.DataFrame()


def save_db(df: pandas.DataFrame):
    df.to_json(db_file_name)
    logger.info(f'saved db to {db_file_name}')


def add_score(df: pandas.DataFrame, name: str, score: int or str):
    row = {'name': name, 'score': score}
    logger.debug(f'[new data]\n {row}')

    # Add data
    merged_df = pd.concat([df, pd.DataFrame(row, index=[0])])
    # Sort data
    sorted_df = sort_rank(merged_df)
    # Trim data
    trimmed_df = drop_losers(sorted_df)
    drop_same_record(trimmed_df)
    # Add Rank column
    ranked_df = add_rank_column(trimmed_df)

    logger.info(f'[data]\n{ranked_df}')
    return ranked_df


def sort_rank(df: pandas.DataFrame):
    df = df.astype({'score': 'int'})
    sorted_df = df.sort_values(by='score', axis=0, ascending=False)
    reset_index(sorted_df)
    return sorted_df


def add_rank_column(df: pandas.DataFrame):
    df['rank'] = range(1, len(df.index)+1)
    df = df[['rank', 'name', 'score']]
    return df


def reset_index(df: pandas.DataFrame):
    df.reset_index(inplace=True, drop=True)
    return


def drop_losers(df: pandas.DataFrame):
    logger.debug(f'dropped rows more than {MAX_USERS_NUM}')
    return df.loc[0:MAX_USERS_NUM-1, :]


def drop_same_record(df: pandas.DataFrame):
    logger.debug(f'dropped overlapping rows')
    # return df.drop_duplicates(['name', 'score'], inplace=True)
    return df.drop_duplicates(['name'], inplace=True)


def gen_html(df: pandas.DataFrame):
    logger.info('generated html_df')
    return df.to_html(index=False, render_links=False)


def compare_score(df: pandas.DataFrame, score:int):
    # New High score
    # Not in ranking board
    pass
############################################################################

if __name__ == '__main__':
    save_db(df_data)

    df_data = add_score(df=df_data, name='kim', score=5)
    df_data = add_score(df=df_data, name='kim1', score=17)
    df_data = add_score(df=df_data, name='kim2', score=8)
    df_data = add_score(df=df_data, name='kim3', score=12)
    print('added\n', df_data)

    df_data = sort_rank(df_data)
    print('sorted\n', df_data)

    df_data = drop_losers(df_data)

    drop_same_record(df_data)
    print('dropped overlapping\n', df_data)
