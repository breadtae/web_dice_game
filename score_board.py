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
     rank | name  | score | dice_count |
        1 |  TAE  | 18    | 3          |
        1 |  MIN  | 18    | 3          |
        2 |  JOE  |  3    | 1          |
"""


MAX_USERS_NUM = 10
db_file_name = 'score.json'


def load_db():
    if os.path.exists(db_file_name):
        logger.info(f'Loaded {db_file_name}')
        return pd.read_json(db_file_name)
    else:
        logger.info('No json file to load')
        return pd.DataFrame()


def save_db(df: pd.DataFrame):
    df.to_json(db_file_name)
    logger.info(f'saved db to {db_file_name}')


def add_score(df: pd.DataFrame, name: str, score: int, dice_count: int = 1):
    row = {'name': name, 'score': score, 'dice_count': dice_count}
    logger.debug(f'[new data]\n {row}')

    merged_df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    sorted_df = sort_rank(merged_df)
    trimmed_df = drop_losers(sorted_df)
    trimmed_df = drop_same_name(trimmed_df)
    ranked_df = add_rank_column(trimmed_df)

    logger.info(f'[data]\n{ranked_df}')
    return ranked_df


def sort_rank(df: pd.DataFrame):
    df = df.copy()
    df = df.astype({'score': 'int'})
    return df.sort_values(by='score', ascending=False).reset_index(drop=True)


def add_rank_column(df: pd.DataFrame):
    """Handles ties: same score = same rank."""
    df = df.copy()
    df['rank'] = df['score'].rank(method='min', ascending=False).astype(int)
    cols = ['rank', 'name', 'score']
    if 'dice_count' in df.columns:
        cols.append('dice_count')
    return df[cols]


def drop_losers(df: pd.DataFrame):
    logger.debug(f'dropped rows more than {MAX_USERS_NUM}')
    return df.iloc[:MAX_USERS_NUM].reset_index(drop=True)


def drop_same_name(df: pd.DataFrame):
    """Keep only the best score per player name."""
    logger.debug('dropped overlapping rows (keep best score per name)')
    return df.drop_duplicates(subset=['name'], keep='first').reset_index(drop=True)


def to_records(df: pd.DataFrame) -> list:
    """Return score data as a list of dicts for template rendering."""
    if df.empty:
        return []
    return df.to_dict('records')
