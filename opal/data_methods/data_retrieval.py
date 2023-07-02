import pandas as pd
from typing import Tuple
from pathlib import Path
from ..constants import DATA_REPO_URL, DATA_LOCAL_STORE


def retrieve_completed_seasons(filename: str, seasons: Tuple[str, ...] = ()) -> pd.DataFrame:
    """Return dataframe of requested completed seasons and filename. Cannot get partial seasons"""
    df_out = pd.DataFrame()
    for s_ in seasons:
        local_path = Path(DATA_LOCAL_STORE)
        local_path.joinpath(filename)
        if not local_path.exists:
            # if no local file then download from url first:
            url_path = Path(DATA_REPO_URL)
            url_path.joinpath(filename)

        df = get_data()
        if df_out.empty:
            df_out = df
        else:
            df_out = pd.concat([df_out, df])
    return df_out


def retrieve_current_season(filename: str, season: str) -> pd.DataFrame:
    """This is different because the season has not completed yet"""
    df_out = pd.DataFrame()
    return df_out


def get_data() -> pd.DataFrame:
    return pd.DataFrame()


if __name__ == '__main__':
    pass

